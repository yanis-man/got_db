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
class Character:

    def __init__(self, char_reference:str) -> None:
        self.api = Api()
        self.char_reference = char_reference
        _raw_data = self.api.get_char(self.char_reference)

        self.name = _raw_data[1]
        self.id = str(_raw_data[0])
        
        self.house = ( House(str(_raw_data[1])) ) if(_raw_data[1] is not None) else House("null")

        _raw_relations = self.api.get_char_relations(self.id)
        self.relations = []

        for _raw_relation in _raw_relations:
            self.relations.append(dict(name = _raw_relation[0], type=_raw_relation[1]))

    def __str__(self) -> str:
        _final_str = f"ID : {self.id} \n Name : {self.name} \n House : {self.house.name} ({self.house.id}) \n Family: \n"
        for member in self.family:
            _final_str += f"\t {member['name']} ({member['id']}) \n"
        _final_str += "RELATIONS :\n"
        for relation in self.relations:
            _final_str += f"\t {relation['house']} -> {relation['type']}"
        return _final_str

