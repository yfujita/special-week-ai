import os
import json
import argparse

from netkeiba.scraper import Scraper

def main():
    arg_parser = argparse.ArgumentParser(description="コマンドライン引数")
    arg_parser.add_argument("--race_id", type=str, help="レースのID", required=True)
    arg_parser.add_argument("--skip_latest", type=str, help="最新レースの成績を除外（過去レース用）", required=False, default=False)
    args = arg_parser.parse_args()

    race_id = args.race_id
    skip_latest = str_to_bool(args.skip_latest)

    scraper = Scraper(race_id = race_id, skip_latest_race_result = skip_latest)
    race_info = scraper.get_race_info()
    
    json_str = json.dumps(race_info.to_dict(), indent=2, ensure_ascii=False)

    with open(f"./output/output_{race_id}.json", "w", encoding="utf-8") as file:
        file.write(json_str)

def str_to_bool(s) -> bool:
    s = s.strip().lower()
    if s in ["true", "1", "t", "y", "yes"]:
        return True
    elif s in ["false", "0", "f", "n", "no"]:
        return False
    else:
        raise ValueError(f"'{s}'はbool値に変換できません。")

if __name__ == '__main__':
    main()