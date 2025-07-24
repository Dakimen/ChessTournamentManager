#import storage_config
from datetime import datetime
import random
from models.player_models import Tournament_Player

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
            if isinstance(match[0], Tournament_Player):
                dict_player1 = {
                    "player_surname": match[0].player.surname,
                    "player_name": match[0].player.name,
                    "player_chess_national_id": match[0].player.chess_national_id
                }
                dict_player2 = {
                    "player_surname": match[1].player.surname,
                    "player_name": match[1].player.name,
                    "player_chess_national_id": match[1].player.chess_national_id}
                match_str_tuple = (dict_player1, dict_player2)
                matches_for_dict.append(match_str_tuple)
            else:
                dict_player1 = {
                    "player_surname": match[0]["player_surname"],
                    "player_name": match[0]["player_name"],
                    "player_chess_national_id": match[0]["player_chess_national_id"]
                }
                dict_player2 = {
                    "player_surname": match[1]["player_surname"],
                    "player_name": match[1]["player_name"],
                    "player_chess_national_id": match[1]["player_chess_national_id"]
                }
                match_str_tuple = (dict_player1, dict_player2)
                matches_for_dict.append(match_str_tuple)
        bye_player = self.get_bye_player()
        if isinstance(bye_player, Tournament_Player):
            bye_player_chess_national_id = bye_player.player.chess_national_id
        else:
            bye_player_chess_national_id = bye_player["player"]["chess_national_id"]
        string_players = []
        if isinstance(self.players[0], Tournament_Player):
            for player in self.players:
                string_player = player.stringify_self()
                string_players.append(string_player)
        else:
            string_players = self.players
        round_dict = {
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "players": string_players,
            "matches": matches_for_dict,
            "bye_player": bye_player_chess_national_id,
            "finished": self.finished,
            "type": self.type
        }
        return round_dict
                
                
class FirstRound(Round):
    def __init__(self, players, matches = [], finished = False, start = None, end = 0, bye_player = None):
        self.name = "Round 1"
        self.players = players
        self.finished = finished
        if start != None:
            self.start_date = start
        else:
            time = datetime.now()
            self.start_date = time.strftime("%H:%M on %d/%m/%Y")
        self.end_date = end
        self.matches = matches
        self.type = "First Round"
        self.bye_player = bye_player

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
    def __init__(self, name, players, matches = [], finished = False, start = None, end = 0, bye_player = None):
        self.name = name
        self.players = players
        self.finished = finished
        if start != None:
            self.start_date = start
        else:
            time = datetime.now()
            self.start_date = time.strftime("%H:%M on %d/%m/%Y")
        self.end_date = end
        self.matches - matches
        self.bye_player = bye_player
        self.type = "Subsequent Round"

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

def recreate_rounds(rounds_list):
    rounds = []
    for round in rounds_list:
        if round["type"] == "First Round":
            recreated_round = FirstRound(round["players"], 
                                         round["matches"], 
                                         round["finished"],
                                         round["start_date"],
                                         round["end_date"],
                                         round["bye_player"])
            rounds.append(recreated_round)
        elif round["type"] == "Subsequent Round":
            recreated_round = SubsequentRound(round["name"],
                                              round["players"],
                                              round["matches"],
                                              round["finished"],
                                              round["start_date"],
                                              round["end_date"],
                                              round["bye_player"])
            rounds.append(recreated_round)
        else:
            raise "Wrong round type"
    return rounds

def update_points(result, match, tournament):
    for tournament_player in tournament.players_list:
        if tournament_player.player.chess_national_id == match[0]["player_chess_national_id"]:
            player1 = tournament_player
        if tournament_player.player.chess_national_id == match[1]["player_chess_national_id"]:
            player2 = tournament_player
    if result == "draw":
        player1.tournament_points += 0.5
        player2.tournament_points += 0.5
    else: 
        if result == player1.player.chess_national_id:
            player1.tournament_points += 1
        if result == player2.player.chess_national_id:
            player2.tournament_points += 1
            