import re
import sys
import time

from bs4 import BeautifulSoup

from .race_info import RaceInfo
from .horse import Horse
from .horse import RaceResult
from . import client

class Scraper:
    def __init__(self, race_id: str, skip_latest_race_result: bool):
        self.race_id = race_id
        self.skip_latest_race_result: bool = skip_latest_race_result

    def get_race_info(self) -> RaceInfo:
        race_url: str = self._build_race_url(self.race_id)
        print('URL:' + race_url)
        response = client.get(race_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        print("Target=" + soup.title.string)

        race_name = self._parse_race_name(soup)
        distance = self._parse_distance(soup)
        course_type = self._parse_course_type(soup)
        mawari = self._parse_mawari(soup)
        horses = self._get_horses(soup)

        #condition = self._parse_condition(soup)
        condition = '不明'

        race_info = RaceInfo(
            race_id = self.race_id,
            race_name = race_name,
            distance = distance,
            course_type = course_type,
            condition = condition,
            mawari = mawari,
            horses = horses
        )
        return race_info
    
    def _parse_race_name(self, soup: BeautifulSoup) -> str:
        return re.findall(r'^(.*?)出馬表', soup.title.string)[0].rstrip()
    
    def _parse_distance(self, soup: BeautifulSoup) -> int:
        soup_distance = soup.find('div', class_='RaceData01')
        distance = int(soup_distance.find('span').text.strip()[1:-1])
        return distance
    
    def _parse_course_type(self, soup: BeautifulSoup) -> str:
        soup_course_type = soup.find('div', class_='RaceData01')
        course_type = soup_course_type.find('span').text.strip()[:1]
        if course_type != '芝' and course_type != 'ダ':
            raise ValueError('Course type is invalid ' + course_type)
        return course_type
    
    def _parse_condition(self, soup: BeautifulSoup) -> str:
        soup_condition = soup.find('div', class_='RaceData01')
        condition = soup_condition.find_all('span', text=re.compile("馬場"))[0].text.strip()[2:][-1]
        if condition != '良' and condition != '稍' and condition != '重' and condition != '不':
            raise ValueError('Condition is invalid ' + condition)
        return condition
    
    def _parse_mawari(self, soup: BeautifulSoup) -> str:
        soup_mawari = soup.find('div', class_='RaceData01')
        mawari = re.findall(r'\((.*?)\)', soup_mawari.text.replace('\xa0C', ''))[0]
        if not mawari.startswith('右') and not mawari.startswith('左') and not mawari.startswith('直線'):
            raise ValueError('Mawari is invalid ' + mawari)
        return mawari
    
    
    def _get_horses(self, soup: BeautifulSoup) -> list[Horse]:
        horses = []

        odds: dict = self._get_odds(self.race_id)

        for tr_horse in soup.find_all('tr', class_='HorseList'):
            td_array = []
            for td in tr_horse.find_all('td'):
                td_array.append(td)

            pos = int(tr_horse.find('td', class_=re.compile('Umaban.')).text.strip())
            td_horseinfo = tr_horse.find('td', class_='HorseInfo')
            horse_name = td_horseinfo.text.strip()

            print('Loading... ' + str(pos) + ':' + horse_name)
            sys.stdout.flush()

            horse_url = td_horseinfo.find('a').get('href')
            race_results = self._scrape_horse(horse_url)
            sex = tr_horse.find('td', class_='Barei').text.strip()[:1]
            age = tr_horse.find('td', class_='Barei').text.strip()[1:]
            body_weight = tr_horse.find('td', class_='Weight').text.strip()
            additional_weight = td_array[5].text.strip()
            jockey = tr_horse.find('td', class_='Jockey').text.strip()

            horse = Horse(
                pos=pos,
                horse_name=horse_name,
                sex=sex,
                age=age,
                body_weight=body_weight,
                additional_weight=additional_weight,
                jockey=jockey,
                race_results=race_results,
                odds = odds[pos]
            )
            horses.append(horse)
            time.sleep(1)

        return horses
    
    def _scrape_horse(self, target_url: str) -> list[RaceResult]:
        response = client.get(target_url)
        soup = BeautifulSoup(response.content, "html.parser")

        soup_result_table = soup.find(class_="db_h_race_results")
        races: list[RaceResult] = []
        is_first = True
        for soup_tr in soup_result_table.find('tbody').find_all("tr"):
            if is_first and self.skip_latest_race_result:
                is_first = False
                print('Skip latest')
                continue
            race_result: RaceResult = self._parse_horse_race_result(soup_tr)
            if race_result != None:
                races.append(race_result)
        return races

    def _parse_horse_race_result(self, soup_tr) -> RaceResult:
        td_array = []
        for soup_td in soup_tr.find_all("td"):
            td_array.append(soup_td)
        if not td_array[11].text.strip().isdigit():
            return None
        return RaceResult(
            date = td_array[0].text.strip(),
            course = td_array[1].text.strip(),
            weather = td_array[2].text.strip(),
            race_name = td_array[4].text.strip(),
            race_grade = td_array[4].get('class')[0] if len(td_array[4].get('class')) > 0 else "",
            number_of_horses = int(td_array[6].text.strip()),
            popularity = td_array[10].text.strip(),
            ranking = int(td_array[11].text.strip()),
            distance = int(td_array[14].text.strip()[1:]),
            course_type = td_array[14].text.strip()[:1],
            course_condition = td_array[15].text.strip(),
            time = td_array[17].text.strip(),
            difference = float(td_array[18].text.strip() if len(td_array[18].text.strip()) > 0 else '0'),
            passing = td_array[20].text.strip(),
            body_weight = td_array[23].text.strip(),
        )
        

    def _build_race_url(self, race_id: str):
        return 'https://race.netkeiba.com/race/shutuba.html?race_id=' + race_id
    
    def _get_odds(self, race_id: str) -> dict:
        response = client.get('https://race.netkeiba.com/api/api_get_jra_odds.html?pid=api_get_jra_odds&input=UTF-8&output=json&type=all&action=init&sort=ninki&compress=0&race_id=' + race_id)

        resp_odds: dict = response.json()['data']['odds']['1']
        result: dict = {}
        for odds_elems in resp_odds.values():
            pos: int = int(odds_elems[3])
            odds: float = float(odds_elems[0])
            result[pos] = odds
        return result
        

