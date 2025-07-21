#import storage_config
from datetime import datetime
import random

class Round:
    def generate_matches(self):
        raise NotImplementedError("This function must be implemented in the subclasses")
    
    def finish_round(self):
        self.finished = True
        self.end_date = datetime.now().strftime("%H:%M on %d/%m/%Y")

    def stringify_matches(self):
        matches_stringified = []
        for match in self.matches:
            new_match = (f"{match[0].player.surname} "
                         f"{match[0].player.name} "
                         f"id: {match[0].player.chess_national_id} " 
                         f"pts: {match[0].tournament_points}"
                         " vs "
                         f"{match[1].player.surname} "
                         f"{match[1].player.name} "
                         f"id: {match[1].player.chess_national_id} " 
                         f"pts: {match[1].tournament_points}") 
            matches_stringified.append(new_match)
        return matches_stringified
    
        
    def get_bye_player(self):
        for player in self.players:
            matches_with_player = [match for match in self.matches if player in match]
            if matches_with_player == []:
                return player
        return None
    
    def get_data(self):
        matches_for_dict = []
        for match in self.matches:
            dict_player1 = {
                "player_surname": match[0].player.surname,
                "player_chess_national_id": match[0].player.chess_national_id
            }
            dict_player2 = {
                "player_surname": match[1].player.surname,
                "player_chess_national_id": match[1].player.chess_national_id}
            match_str_tuple = (dict_player1, dict_player2)
            matches_for_dict.append(match_str_tuple)
        bye_player = self.get_bye_player()
        round_dict = {
            "name": self.name,
            "start_date": self.start_date,
            "matches": matches_for_dict,
            "bye_player": bye_player.player.chess_national_id,
            "finished": self.finished
        }
        return round_dict
                


    """def stringfy_round(self):
        own_data = {
            "start_date": self.start_date,
            "matches": 
        }"""

class FirstRound(Round):
    def __init__(self, players):
        self.name = "Round 1"
        self.players = players
        self.finished = False
        time = datetime.now()
        self.start_date = time.strftime("%H:%M on %d/%m/%Y")
        self.end_date = 0
        self.matches = None

    def generate_matches(self):
        random.shuffle(self.players)
        generated_matches = list(zip(self.players[::2], self.players[1::2]))
        self.matches = generated_matches

    def get_bye_player(self):
        return super().get_bye_player()

    def stringify_matches(self):
        return super().stringify_matches()

    def finish_round(self):
         super().finish_round()

    def get_data(self):
        return super().get_data()

class SubsequentRound(Round):
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.finished = False
        time = datetime.now()
        self.start_date = time.strftime("%H:%M on %d/%m/%Y")
        self.end_date = 0
        self.matches = []

    def generate_matches(self, match_history):
        pass
        """sorted_players = sorted(self.players, key=lambda p: p.tournament_points, reverse=True)"""

    def get_bye_player(self):
        return super().get_bye_player()
    
    def stringify_matches(self):
        return super().stringify_matches()

    def finish_round(self):
         super().finish_round()

    def get_data(self):
        return super().get_data()




