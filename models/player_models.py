import storage_config as storage_config
import re
from tinydb import Query

class Player:
    def __init__(self, player_info):
        self.name = player_info["player_name"]
        self.surname = player_info["player_surname"]
        self.date_of_birth = player_info["date_of_birth"]
        self.chess_national_id = player_info["chess_national_id"]

    def save_player(self):
        """Saves player to the database"""
        storage_config.PLAYER_DB.insert({
            "name": self.name,
            "surname": self.surname,
            "date_of_birth": self.date_of_birth,
            "chess_national_id": self.chess_national_id
        })
        return True
    
class Tournament_Player(Player):
    def __init__(self, surname, name, chess_national_id, date_of_birth=""):
        self.surname = surname
        self.name = name
        self.chess_national_id = chess_national_id 
        self.date_of_birth = date_of_birth
        self.tournament_points = 0

    def save_player(self, date_of_birth):
        """Adds player to the database, called if he's not there when creating a tournament, requires a date of birth"""
        self.date_of_birth = date_of_birth
        return super().save_player()
    
    def check_if_in_db(self):
        all_players = list_all_players()
        for one_player in all_players:
            if one_player["surname"] == self.surname and one_player["name"] == self.name:
                if one_player["chess_national_id"] == self.chess_national_id:
                    return True
        return False
        

    

def list_all_players():
    list_of_all_players = storage_config.PLAYER_DB.all()
    return list_of_all_players

def check_chess_id_validity(new_player_id, all_chess_ids):
    pattern = r"^[A-Z]{2}\d{5}$"
    if new_player_id in all_chess_ids:
        return False
    if re.match(pattern, new_player_id) is None:
        return False
    return True

def sort_players_alphabetically(players_to_sort):
    sorted_players = sorted(players_to_sort, key=lambda p: p["surname"])
    return sorted_players

def check_if_in_db(new_player):
    Player_existant = Query()
    if storage_config.PLAYER_DB.search(Player_existant.surname == f"{new_player["player_surname"]}") != []:
        if storage_config.PLAYER_DB.search(Player_existant.chess_national_id == f"{new_player["chess_national_id"]}"):
            return True
    return False
