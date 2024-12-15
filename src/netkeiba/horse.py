class Horse:
    def __init__(self, pos: int, horse_name: str, sex: str, age: int, body_weight: str, additional_weight: int, jockey: str, race_results: list, odds: float):
        self.pos: int = pos
        self.horse_name: str = horse_name
        self.sex: str = sex
        self.age: int = age
        self.body_weight: str = body_weight
        self.additional_weight: int = additional_weight
        self.jockey: str = jockey
        self.race_results: list = race_results 
        self.odds: float = odds

    def getRunType(self) -> str:
        position = 0
        for race_result in self.race_results:
            if race_result.passing == '':
                continue
            first_passing = race_result.passing.split('-')[0]
            position += int(first_passing) / race_result.number_of_horses

        position = position / len(self.race_results)
        if position <= 0.2:
            return '逃げ'
        elif position <= 0.4:
            return '先行'
        elif position <= 0.7:
            return '差し'
        else:
            return '追込'
    
    def to_dict(self) -> dict:
        dic :dict = {}
        dic['pos'] = self.pos
        dic['horse_name'] = self.horse_name
        dic['sex'] = self.sex
        dic['age'] = self.age
        dic['body_weight'] = self.body_weight
        dic['run_type'] = self.getRunType()
        dic['additional_weight'] = self.additional_weight
        dic['jockey'] = self.jockey
        dic['odds'] = self.odds
        dic['race_results'] = [result.to_dict() for result in self.race_results]
        return dic

class RaceResult:
    def __init__(self,
        date: str,
        course: str,
        weather: str,
        race_name: str,
        race_grade: str,
        number_of_horses: int,
        popularity: str,
        ranking: int,
        distance: int,
        course_type: str,
        course_condition: str,
        time: str,
        difference: float,
        passing: str,
        body_weight: str
        ):
        
        self.date: str = date
        self.course: str = course
        self.weather: str = weather
        self.race_name: str = race_name
        self.race_grade: str = race_grade
        self.number_of_horses: int = number_of_horses
        self.popularity: str = popularity
        self.ranking: int = ranking
        self.distance: int = distance
        self.course_type: str = course_type
        self.course_condition: str = course_condition
        self.time: str = time
        self.difference: float = difference
        self.passing: str = passing
        self.body_weight: str = body_weight

    def to_dict(self) -> dict:
        dic :dict = {}
        dic['日付'] = self.date
        #dic['コース'] = self.course
        #dic['天気'] = self.weather
        dic['レース名'] = self.race_name
        #dic['グレード'] = self.race_grade
        #dic['出走頭数'] = self.number_of_horses
        #dic['人気'] = self.popularity
        dic['着順'] = self.ranking
        dic['距離'] = self.distance
        dic['コース種別'] = self.course_type
        #dic['コースコンディション'] = self.course_condition
        #dic['時計'] = self.time
        dic['着差'] = self.difference
        #dic['途中通過順位'] = self.passing
        dic['馬体重'] = self.body_weight
        
        return dic

