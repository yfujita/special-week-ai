from .horse import Horse


class RaceInfo:
    def __init__(self, race_id: str, race_name: str, distance: int, course_type: str, condition: str, mawari: str, horses: list[Horse]):
        self.race_id = race_id
        self.race_name = race_name
        self.distance = distance
        self.course_type = course_type
        self.condition = condition
        self.mawari = mawari
        self.horses = horses
    
    def to_dict(self) -> dict:
        dic: dict = {}
        dic['race_id']  = self.race_id
        dic['race_name'] = self.race_name
        dic['distance'] = self.distance
        dic['course_type'] = self.course_type
        dic['condition'] = self.condition
        dic['mawari'] = self.mawari
        dic['horses'] = [horse.to_dict() for horse in self.horses]

        return dic





