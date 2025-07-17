from tinydb import TinyDB, Query
import re

player_db = TinyDB("player_database.json")
tournament_db = TinyDB("tournament_database.json")
class Player:
    def __init__(self, player_info):
        self.name = player_info["player_name"]
        self.surname = player_info["player_surname"]
        self.date_of_birth = player_info["date_of_birth"]
        self.chess_national_id = player_info["chess_national_id"]

    def save_player(self):
        player_db.insert({
            "name": self.name,
            "surname": self.surname,
            "date_of_birth": self.date_of_birth,
            "chess_national_id": self.chess_national_id
        })
        return True

def list_all_players():
    list_of_all_players = player_db.all()
    return list_of_all_players

def check_chess_id_validity(new_player_id, all_chess_ids):
    pattern = r"^[A-Z]{2}\d{5}$"
    if new_player_id in all_chess_ids:
        return False
    if re.match(pattern, new_player_id) is None:
        return False
    return True



class Tournament:
    def __init__(self, tournament_data):
        self.name = tournament_data["tournament_name"]
        self.place = tournament_data["tournament_place"]
        self.beginning_date = tournament_data["tournament_beginning_date"]
        self.end_date = tournament_data["tournament_end_date"]
        self.registered_players_surnames = tournament_data["registered_players_surnames"]
        self.description = tournament_data["tournament_description"]
        if tournament_data["number_of_rounds"] is "":
            tournament_data["number_of_rounds"] = "4"
        self.number_of_rounds = tournament_data["number_of_rounds"]
        

class Round:
    pass

        
