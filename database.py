from sqlite3 import connect
import re as Regex

class Database:
    
    def __init__(self) -> None:
        self.connection = connect("./got_chars.db")
        self.cursor = self.connection.cursor()
    
    def __del__(self) -> None:
        try:
            self.cursor.close()
        except:
            print("Error while closing the cursor")
        
        try:
            self.connection.commit()
            self.connection.close()
        except:
            print("Error while closing the DB")
    
    def save_to_db(self, QUERY: str, params : tuple):
        self.cursor.execute(QUERY, params)
    # utilitary function to execute a query which pulls from the DB
    def pull_from_db(self, QUERY : str, params : tuple = (), only_first = False, order_by = None):
        query = QUERY
        if order_by is not None:
            query = f'{QUERY} ORDER BY {order_by} ASC'

        self.cursor.execute(query, params)
        
        if only_first:
            return self.cursor.fetchone()
        
        return self.cursor.fetchall() 

class Api(Database):
    
    def __init__(self) -> None:
        super().__init__()
    
    def __del__(self) -> None:
        return super().__del__()
    

    # since the database can be searched using names and id, this utility function ensure the choose between both in order to execute the correct query
    def _is_id_search(self, reference:str):
        if Regex.match("[0-9]{1,2}",
        
         reference):
            return True
        # the search is based on text
        return False

    ##########################################################
    # HOUSES METHODS
    ##########################################################

    def create_house(self, house_name:str):
        # avoid non houses addition
        if not Regex.match("House", house_name):
            return
        QUERY = "INSERT INTO houses (display_name) VALUES (?)"
        self.save_to_db(QUERY, (house_name,))
        
    def get_house(self, house_reference : str):
        # check if we want to get a house based on the id
        if self._is_id_search(house_reference):
            house_reference = int(house_reference)
            return self.pull_from_db('SELECT * FROM houses WHERE id=?', (house_reference,), only_first=True)
        
        # the house is referenced as a name
        return self.pull_from_db(f'SELECT * FROM houses WHERE display_name LIKE "%{house_reference}%"', only_first=True)

        # get a house from : id or name
    ##########################################################
    # CHARACTERS METHODS
    ##########################################################
    def create_char(self, name:str, house_id:int):
        QUERY = "INSERT INTO characters (display_name, house_id, father_id, mother_id) VALUES (?, ?, ?, ?)"

        self.save_to_db(QUERY, (name, house_id, 1, 1))

        return self.cursor.lastrowid

    def update_char_parents(self, char_reference:str, parent_choice:str, parent_id:str):
        if self._is_id_search(char_reference):
            char_reference = int(char_reference)
            self.save_to_db(f"UPDATE characters SET {parent_choice}_id = ? WHERE id = ?;", (parent_id, char_reference))
            return
        
        self.save_to_db(f"UPDATE characters SET {parent_choice}_id = ? WHERE display_name LIKE '%{char_reference}%'", (parent_id,))
        return

        

    def get_char(self, char_reference: str):
        if self._is_id_search(char_reference):
            char_reference = int(char_reference)
            return self.pull_from_db("SELECT * FROM characters WHERE id = ?", params=(char_reference,), only_first=True)
        
        return self.pull_from_db(f'SELECT * FROM characters WHERE display_name LIKE "%{char_reference}%"', only_first=True)

    def get_chars_list(self):
        return self.pull_from_db("SELECT * FROM characters")
    
    def get_char_family(self, house_id:int):
        return self.pull_from_db("SELECT * FROM characters WHERE house_id = ? ORDER BY display_name ASC;", (house_id,))
    ##########################################################
    #RELATIONS METHODS
    ##########################################################

    # create a relation (vassal / servant)
    def create_char_house_relation(self, char_id:int, house_id:int, relation_id:int):
        QUERY = "INSERT INTO chars_houses_relations (house_id, char_id, relation_id) VALUES (?,?,?);"
        self.save_to_db(QUERY, (house_id, char_id, relation_id))

    def create_char_to_char_relation(self, char_1:int, char_2:int, relational_kw:str):
        # gets the id of the relation type
        relation_type_id = self.pull_from_db("SELECT id FROM char_relations_types WHERE relational_keyword = ?", (relational_kw,), only_first=True)
        # the relation is special or not know -> it gets the "default" relation type (other)
        if relation_type_id is None:
            relation_type_id = self.pull_from_db("SELECT id FROM char_relations_types WHERE relational_keyword='other';", only_first=True)

        self.save_to_db("INSERT INTO char_relations (char_1_id, char_2_id, relation_type) VALUES (?,?,?)", (char_1, char_2, relation_type_id[0]))

    def get_char_family(self, char_reference : int):
        QUERY1 = """
                SELECT 
                    char_relations.id,
	                characters.display_name as char_name,
	                char_relations_types.display_name as relation_name,
                	relation_type,
                    char_2_id 
                FROM 
                	char_relations
                INNER JOIN
                	characters
                	ON char_2_id = characters.id
                INNER JOIN
                	char_relations_types
                	ON relation_type = char_relations_types.id
                WHERE 
                	char_1_id = ?;"""
        QUERY2 = """
                SELECT 
                    char_relations.id,
	                characters.display_name as char_name,
	                char_relations_types.display_name as relation_name,
                	relation_type,
                    char_1_id 
                FROM 
                	char_relations
                INNER JOIN
                	characters
                	ON char_1_id = characters.id
                INNER JOIN
                	char_relations_types
                	ON relation_type = char_relations_types.id
                WHERE 
                	char_2_id = ?;"""
        _family = self.pull_from_db(QUERY1, (char_reference,))
        _family += self.pull_from_db(QUERY2, (char_reference,))

        final_family = []

        for family in _family:
            print(family, end="\n")
                

        return _family

    
    def get_char_house_relation(self, char_reference:int):
        QUERY = """SELECT
                        characters.display_name as char_name,
                	    houses.display_name as house_name,
                	    chars_houses_relations_types.display_name as relation
                    FROM
                	    chars_houses_relations

                    INNER JOIN characters
                    ON characters.id = char_id

                    INNER JOIN houses
                    ON houses.id = chars_houses_relations.house_id

                    INNER JOIN chars_houses_relations_types
                    ON chars_houses_relations_types.id = relation_id
                    WHERE char_id = ?;"""
        
        return self.pull_from_db(QUERY, (char_reference,))