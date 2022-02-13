from database import Api
import requests
from bs4 import BeautifulSoup
import re as Regex

def populate_data():
    api = Api()

    # retrieve the raw html
    raw_html_page = requests.get("https://en.wikipedia.org/wiki/List_of_A_Song_of_Ice_and_Fire_characters").content
    parsed_html = BeautifulSoup(raw_html_page, 'html.parser')

    char_list = {}

    # gets the global array
    raw_elements = parsed_html.find("div", {'class':'mw-parser-output'})
    isFamily = 1

    for element in raw_elements:
        # retrieve if possible the value of the element
        try:
            element_value = str.strip(element.find('span').text)
        except:
            element_value = None
        
        # house balise
        if element.name == "h2":
            # gets 
            current_house = element_value
            api.create_house(element_value)

        #entering a character balise
        elif element.name == "h4":

            current_character = element_value
            char_data = dict(name=current_character, house=None)
            # chracter is listed as family member
            house_id = api.get_house(current_house)
            # some don't have houses ensure it to be null
            char_data['house'] = (house_id[0] if(house_id != None) else None)
            if not isFamily:
                # if we arent listing family member (given by isFamily value) the char needs to be added to the 
                current_character_data = api.get_char(current_character)
                if current_character_data is None:
                    current_char_id = api.create_char(char_data['name'], char_data['house'])
                api.create_char_house_relation(current_char_id, char_data["house"], 1)
            else:
                api.create_char(char_data['name'], char_data['house'])

            
        # check if we're looking @ family members 
        elif element.name == "h3":
            element_value = element_value
            if element_value != 'Family' and isFamily:
                isFamily = 0
            else:
                isFamily = 1

def populate_char_relations():
    
    api = Api()
    BASE_URL = "https://en.m.wikipedia.org/wiki/"
    characters_list = api.get_chars_list()

    for char in characters_list:
        parsed_char_name = Regex.sub("[\s]+", "_", char[2])
        char_raw_html = requests.get(BASE_URL+parsed_char_name)

        try:
            char_raw_html = char_raw_html.content
        except:
            continue

        parsed_char_html = BeautifulSoup(char_raw_html, "html.parser")

        relatives_array = parsed_char_html.find('th', text="Relatives")
        if relatives_array is None:
            continue
        try:
            relatives_array = relatives_array.parent.find('div', {'class':'plainlist'}).find_all('li') 
        except:
            continue  
        for relative in relatives_array:
            relative_data = {}
            # the relative character have a link to his page
            _raw_relative_data = relative.text.split("(")
            if len(_raw_relative_data) < 2:
                continue

            relative_db_data = api.get_char(str.strip(_raw_relative_data[0]))
            # the character's relative may not be in the db, this fix it
            if relative_db_data is None:
                relative_data['id'] = api.create_char(str.strip(_raw_relative_data[0]), char[1])
            else:
                relative_data['id'] = relative_db_data[0]
            relative_data['relational_keyword'] = _raw_relative_data[1].replace(')', '', 1)

            # we found stromae's father
            if relative_data['relational_keyword'] == "father" or relative_data['relational_keyword'] == "mother":
                api.update_char_parents(str(char[0]), relative_data['relational_keyword'], str(relative_data['id']))
            else:
                api.create_char_to_char_relation(str(char[0]), str(relative_data['id']), relative_data['relational_keyword'])