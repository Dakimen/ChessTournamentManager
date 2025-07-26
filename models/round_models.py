from datetime import datetime
import random
from models.player_models import Tournament_Player, Player, get_player_from_db

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
                return player.player.chess_national_id
        return None
    
    def get_data(self):
        matches_for_dict = []
        for match in self.matches:
            dict_player1 = [{
                "player_surname": match[0].player.surname,
                "player_name": match[0].player.name,
                "chess_national_id": match[0].player.chess_national_id
                },
                 match[0].tournament_points
            ]
            dict_player2 = [{
                "player_surname": match[1].player.surname,
                "player_name": match[1].player.name,
                "chess_national_id": match[1].player.chess_national_id
                },
                match[1].tournament_points]
            match_str_tuple = (dict_player1, dict_player2)
            matches_for_dict.append(match_str_tuple)
        bye_player = self.get_bye_player()
        string_players = []
        for player in self.players:
            string_player = player.stringify_self()
            string_players.append(string_player)
        round_dict = {
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "players": string_players,
            "bye_history": self.bye_history,
            "matches": matches_for_dict,
            "bye_player": bye_player,
            "finished": self.finished,
            "type": self.type
        }
        return round_dict
    
    def recreate_matches(self):
        matches = []
        for match in self.matches:
            player1_info = get_player_from_db(match[0][0])
            player2_info = get_player_from_db(match[1][0])
            player1_obj = Player(player1_info)
            player2_obj = Player(player2_info)
            tourn_player1 = Tournament_Player(player1_obj, match[0][1])
            tourn_player2 = Tournament_Player(player2_obj, match[1][1])
            new_match = (tourn_player1, tourn_player2)
            matches.append(new_match)
        self.matches = matches
    
    def recreate_players(self):
        players = []
        for player in self.players:
            player_obj = Player(player["player"])
            t_player = Tournament_Player(player_obj, player["tournament_points"])
            players.append(t_player)
        self.players = players
                
                
class FirstRound(Round):
    def __init__(self, players, bye_history, matches = [], finished = False, start = None, end = 0, bye_player = None):
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
        self.bye_history = bye_history

    def generate_matches(self):
        random.shuffle(self.players)
        generated_matches = list(zip(self.players[::2], self.players[1::2]))
        self.matches = generated_matches

class SubsequentRound(Round):
    def __init__(self, name, players, bye_history, matches = [], finished = False, start = None, end = 0, bye_player = None):
        self.name = name
        self.players = players
        self.finished = finished
        if start != None:
            self.start_date = start
        else:
            time = datetime.now()
            self.start_date = time.strftime("%H:%M on %d/%m/%Y")
        self.end_date = end
        self.matches = matches
        self.bye_history = bye_history
        self.bye_player = bye_player
        self.type = "Subsequent Round"

    def get_bye_players_as_objects(self):
        bye_players= []
        for bye_player_id in self.bye_history:
            bye_player_data = {"chess_national_id": bye_player_id}
            bye_player_data = get_player_from_db(bye_player_data)
            bye_player_obj = Player(bye_player_data)
            bye_player_obj = Tournament_Player(bye_player_obj, 0)
            bye_players.append(bye_player_obj)
        return bye_players
    
    def generate_sorted_players(self):
        players_with_points = []
        self.matches = []
        for player in self.players:
            player_with_points = (player, player.tournament_points)
            players_with_points.append(player_with_points)
        sorted_players = sorted(players_with_points, key=lambda x: x[1], reverse=True)
        return sorted_players
    
    def generate_matches(self, match_history):
        sorted_players = self.generate_sorted_players()
        used = set()
        for i, (player, _) in enumerate(sorted_players):
            if player in used:
                continue

            for j in range(i + 1, len(sorted_players)):
                opponent, _ = sorted_players[j]
                if opponent in used:
                    continue

                if not have_played(player, opponent, match_history):
                    self.matches.append((player, opponent))
                    used.add(player)
                    used.add(opponent)
                    break

    def generate_matches_with_bye(self, match_history):
        sorted_players = self.generate_sorted_players()
        used = set()
        bye_players = self.get_bye_players_as_objects()
        n_of_matches = int((len(self.players) - 1) / 2)
        n_of_bye_players = len(bye_players)
        
        def check_bye_player_in_matches(bye_player_id):
            matches = self.matches
            for match in matches:
                (player1, player2) = match
                if player1.player.chess_national_id == bye_player_id:
                    return True
                elif player2.player.chess_national_id == bye_player_id:
                    return True
                else:
                    return False

        
        def check_bye_players(p1, p2):
            all_present = True
            for bye_player in bye_players:
                if  p1.player.chess_national_id == bye_player.player.chess_national_id:
                    continue
                elif p2.player.chess_national_id == bye_player.player.chess_national_id:
                    continue
                elif check_bye_player_in_matches(bye_player.player.chess_national_id):
                    continue
                else:
                    all_present = False
            return all_present
            

        
        for i, (player, _) in enumerate(sorted_players):
            if player in used:
                continue

            for j in range(i + 1, len(sorted_players)):
                opponent, _ = sorted_players[j]
                if opponent in used:
                    continue

                if not have_played(player, opponent, match_history):
                    if len(self.matches) == n_of_matches - n_of_bye_players:
                        if check_bye_players(player, opponent):
                            self.matches.append((player, opponent))
                            used.add(player)
                            used.add(opponent)
                            break
                        else:
                            break
                    self.matches.append((player, opponent))
                    used.add(player)
                    used.add(opponent)
                    break

        for player, _ in sorted_players:
            if player not in used:
                self.bye_player = player.player.chess_national_id
                break

def recreate_rounds(rounds_list):
    rounds = []
    for round in rounds_list:
        if round["type"] == "First Round":
            recreated_round = FirstRound(round["players"],
                                         round["bye_history"],
                                         round["matches"],
                                         round["finished"],
                                         round["start_date"],
                                         round["end_date"],
                                         round["bye_player"])
            rounds.append(recreated_round)
        elif round["type"] == "Subsequent Round":
            recreated_round = SubsequentRound(round["name"],
                                              round["players"],
                                              round["bye_history"],
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
        if tournament_player.player.chess_national_id == match[0].player.chess_national_id:
            player1 = tournament_player
        if tournament_player.player.chess_national_id == match[1].player.chess_national_id:
            player2 = tournament_player
    if result == "draw":
        player1.tournament_points += 0.5
        player2.tournament_points += 0.5
    else: 
        if result == player1.player.chess_national_id:
            player1.tournament_points += 1
        elif result == player2.player.chess_national_id:
            player2.tournament_points += 1

def have_played(p1, p2, match_history):
    return (p1, p2) in match_history or (p2, p1) in match_history
            