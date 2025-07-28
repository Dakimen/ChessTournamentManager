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
    def __init__(self, player: Player, tournament_id, player_tournament_points = 0):
        self.player = player
        self.tournament_points = player_tournament_points
        self.tournament_id = tournament_id

    def __eq__(self, other):
        if isinstance(other, Tournament_Player):
            return self.tournament_id == other.tournament_id
        else:
            return False

    def __hash__(self):
        return hash(self.tournament_id)
    
    def __repr__(self):
        return f"{self.player.surname}"

    def get_player_score_list(self):
        player_score = [self.player.stringify_self(), self.tournament_points]
        return player_score
    
    def stringify_self(self):
        self_dict = {
            "player":
            {"player_name": self.player.name,
            "player_surname": self.player.surname,
            "date_of_birth": self.player.date_of_birth,
            "chess_national_id": self.player.chess_national_id},
            "tournament_points": self.tournament_points,
            "tournament_id": self.tournament_id
        }
        return self_dict
    

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
    sorted_players = sorted(players_to_sort, key=lambda p: p["player_surname"])
    return sorted_players


def check_if_in_db(new_player):
    existant_player = Query()
    if storage_config.PLAYER_DB.search(existant_player.player_surname == f"{new_player["player_surname"]}") != []:
        if storage_config.PLAYER_DB.search(existant_player.chess_national_id == f"{new_player["chess_national_id"]}"):
            return True
    return False

def get_player_from_db(player_data):
    player_in_db = Query()
    player_found = storage_config.PLAYER_DB.search(player_in_db.chess_national_id == f"{player_data["chess_national_id"]}")
    return player_found[0] #player_found is a list containing a dict, we only need the dict

def get_participating_players_from_data(tourn_data):
    player_tuples = []
    for player in tourn_data["players_list_raw"]:
        player_obj = Player(player["player"])
        player_tournament_id = player["tournament_id"]
        player_points = player["tournament_points"]
        player_tuple = (player_obj, player_tournament_id, player_points)
        player_tuples.append(player_tuple)
    return player_tuples
