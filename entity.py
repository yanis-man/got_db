class House:
    def __init__(self, id:int, name:str) -> None:
        self.id = id
        self.name = name

class Character:

    def __init__(self, id:int, name:str, house:House, family:dict, relations:dict) -> None:
        self.id = id
        self.name = name
        self.house = house
        self.family = family
        self.relations = relations
    def __str__(self) -> str:
        _final_str = f"ID : {self.id} \n Name : {self.name} \n House : {self.house.name} ({self.house.id}) \n Family: \n"
        for member in self.family:
            _final_str += f"\t {member['name']} ({member['id']}) \n"
        _final_str += "RELATIONS :\n"
        for relation in self.relations:
            _final_str += f"\t {relation['house']} -> {relation['type']}"
        return _final_str
