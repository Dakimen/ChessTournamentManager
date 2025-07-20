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
            "player_name": self.name,
            "player_surname": self.surname,
            "date_of_birth": self.date_of_birth,
            "chess_national_id": self.chess_national_id
        })
        return True
    
    def stringify_self(self):
        self_dict = {
            "player_name": self.name,
            "player_surname": self.surname,
            "date_of_birth": self.date_of_birth,
            "chess_national_id": self.chess_national_id
        }
        return self_dict
    
class Tournament_Player:
    def __init__(self, player: Player):
        self.player = player
        self.tournament_points = 0

    def get_player_score_list(self):
        player_score = [self.player.stringify_self(), self.tournament_points]
        return player_score
        

    

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
