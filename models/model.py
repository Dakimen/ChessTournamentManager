import storage_config as storage_config
import re

class Player:
    def __init__(self, player_info):
        self.name = player_info["player_name"]
        self.surname = player_info["player_surname"]
        self.date_of_birth = player_info["date_of_birth"]
        self.chess_national_id = player_info["chess_national_id"]

    def save_player(self):
        storage_config.PLAYER_DB.insert({
            "name": self.name,
            "surname": self.surname,
            "date_of_birth": self.date_of_birth,
            "chess_national_id": self.chess_national_id
        })
        return True

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



class Tournament:
    def __init__(self, tournament_data):
        self.name = tournament_data["tournament_name"]
        self.place = tournament_data["tournament_place"]
        self.dates = f"{tournament_data["tournament_beginning_date"]} - {tournament_data["tournament_end_date"]}"
        self.description = tournament_data["tournament_description"]
        if tournament_data["number_of_rounds"] is "":
            tournament_data["number_of_rounds"] = "4"
        self.number_of_rounds = tournament_data["number_of_rounds"]
        self.rounds = None #for now
        self.players_list = None #for now

    def save_tournament(self):
        storage_config.TOURNAMENT_DB.insert({
            "name": self.name,
            "place": self.place,
            "dates": self.dates,
            "description": self.description,
            "number_of_rounds": self.number_of_rounds
        })
        

class Round:
    def __init__(self):
        pass

        
