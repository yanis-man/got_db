from scrapper import populate_data, populate_char_relations
from entity import House, Character

if __name__ == "__main__":
###
# MUST BE UNCOMMENTED IF YOU WANT TO FILL THE DATABASE
##
    #populate_data()
    #populate_char_relations()
    QUIT = False
    while(not QUIT):
        print("Prochaine action ? \n 1. Rechercher un personnage 2. Rechercher une maison 3. Quitter")
        user_choice = int(input())

        # user wants to search among characets
        if user_choice == 1:
            print("Nom ou ID du personnage:")
            user_target = input()
            character = Character(user_target)
            print(character)
        # user wants to search among houses
        if user_choice == 2:
            print("Nom ou ID")
            target_house = input()
            house = House(target_house)
            print(house)
