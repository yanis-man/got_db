from database import Api

class House:
    def __init__(self, house_reference:str) -> None:
        self.api = Api()
        if house_reference == "null":
            self.id = "Aucune"
            self.name = 0
        else:
            _raw_data = self.api.get_house(house_reference)

            self.id = _raw_data[0]
            self.name = _raw_data[1]
    
    def __str__(self):
        _final_str = f"{self.name} ({self.id})"
        return _final_str
class Character:

    def __init__(self, char_reference:str) -> None:
        self.api = Api()
        self.char_reference = char_reference
        # retrieve the character's data
        _raw_data = self.api.get_char(self.char_reference)
        self.name = _raw_data[2]
        self.id = str(_raw_data[0])

        #initialize a house object depending on the character family
        self.house = ( House(str(_raw_data[1])) ) if(_raw_data[1] is not None) else House("null")

        _raw_family = self.api.get_char_family(self.id)
        print(_raw_family)
        self.family = []

        for member in _raw_family:
            self.family.append(dict(name = member[1], id=member[4], type=member[2]))

        _raw_relations = self.api.get_char_house_relation(self.house.id)
        self.relations = []
        if len(_raw_relations) > 0:
            self.relations = []
            for relation in _raw_relations:
                self.relations.append(dict(house=member[1], type=relation[1]))

    def __str__(self) -> str:
        _final_str = f"ID : {self.id} \nName : {self.name} \nHouse : {self.house.name} ({self.house.id}) \nFamily: \n"
        for member in self.family:
            _final_str += f"\t{member['name']} -> {member['type']} ({member['id']}) \n"
        _final_str += "Relations :\n"
        for relation in self.relations:
            _final_str += f"\t{relation['house']} -> {relation['type']}"
        return _final_str

