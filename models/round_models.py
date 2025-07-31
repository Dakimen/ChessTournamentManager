from datetime import datetime
import random
from models.player_models import Tournament_Player, Player, get_player_from_db


class Round:
    def generate_matches(self):
        raise NotImplementedError(
            "This function must be implemented in the subclasses"
            )

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

    def get_data(self):
        matches_for_dict = []
        for match in self.matches:
            dict_player1 = [{
                "player_surname": match[0].player.surname,
                "player_name": match[0].player.name,
                "chess_national_id": match[0].player.chess_national_id
                },
                match[0].tournament_id,
                match[0].tournament_points
            ]
            dict_player2 = [{
                "player_surname": match[1].player.surname,
                "player_name": match[1].player.name,
                "chess_national_id": match[1].player.chess_national_id
                },
                match[1].tournament_id,
                match[1].tournament_points]
            match_str_tuple = (dict_player1, dict_player2)
            matches_for_dict.append(match_str_tuple)
        string_players = []
        for player in self.players:
            string_player = player.stringify_self()
            string_players.append(string_player)
        if isinstance(self.removed_player, int):
            self.recreate_removed_player()
        round_dict = {
            "name": self.name,
            "number": self.number,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "players": string_players,
            "matches": matches_for_dict,
            "finished": self.finished,
            "type": self.type,
            "removed_player": self.removed_player.tournament_id
        }
        return round_dict

    def recreate_matches(self):
        matches = []
        for match in self.matches:
            player1_info = get_player_from_db(match[0][0])
            player2_info = get_player_from_db(match[1][0])
            player1_obj = Player(player1_info)
            player2_obj = Player(player2_info)
            tourn_player1 = Tournament_Player(player1_obj,
                                              match[0][1],
                                              match[0][2])
            tourn_player2 = Tournament_Player(player2_obj,
                                              match[1][1],
                                              match[1][2])
            new_match = (tourn_player1, tourn_player2)
            matches.append(new_match)
        self.matches = matches

    def recreate_players(self):
        players = []
        for player in self.players:
            player_obj = Player(player["player"])
            t_player = Tournament_Player(player_obj,
                                         player["tournament_id"],
                                         player["tournament_points"])
            players.append(t_player)
        self.players = players

    def recreate_removed_player(self):
        for player in self.players:
            if player.tournament_id == self.removed_player:
                self.removed_player = player


class FirstRound(Round):
    def __init__(self, players, matches=[], finished=False, start=None,
                 end=0, removed_player=None):
        self.name = "Round 1"
        self.players = players
        self.number = 1
        self.finished = finished
        if start is None:
            self.start_date = start
        else:
            time = datetime.now()
            self.start_date = time.strftime("%H:%M on %d/%m/%Y")
        self.end_date = end
        self.matches = matches
        self.type = "First Round"
        self.removed_player = removed_player

    def generate_matches(self):
        players_copy = self.players[:]
        if len(players_copy) % 2 != 0:
            for player in players_copy:
                if player.tournament_id == 0:
                    players_copy.remove(player)
                    self.removed_player = player
        random.shuffle(players_copy)
        generated_matches = list(zip(players_copy[::2], players_copy[1::2]))
        self.matches = generated_matches


class SubsequentRound(Round):
    def __init__(self, name, players, number, matches=[], finished=False,
                 start=None, end=0, removed_player=None):
        self.name = name
        self.players = players
        self.number = number
        self.finished = finished
        if start is not None:
            self.start_date = start
        else:
            time = datetime.now()
            self.start_date = time.strftime("%H:%M on %d/%m/%Y")
        self.end_date = end
        self.matches = matches
        self.type = "Subsequent Round"
        self.removed_player = removed_player

    def generate_sorted_players(self, players_copy):
        players_with_points = []
        self.matches = []
        for player in players_copy:
            player_with_points = (player, player.tournament_points)
            players_with_points.append(player_with_points)
        sorted_players = sorted(players_with_points, key=lambda x: x[1],
                                reverse=True)
        return sorted_players

    def generate_matches(self, match_history, removed_list):
        players_copy = self.players[:]
        if len(players_copy) % 2 != 0:
            candidates = [
                (to_remove, [p for p in players_copy if p != to_remove])
                for to_remove in players_copy
                if to_remove not in removed_list]
            for removed_player, candidate_players in candidates:
                self.matches = []
                sorted_players = self.generate_sorted_players(candidate_players)
                used = set()
                success = True
                for i, (player, _) in enumerate(sorted_players):
                    if player in used:
                        continue
                    found = False
                    for j in range(i + 1, len(sorted_players)):
                        opponent, _ = sorted_players[j]
                        if opponent in used:
                            continue
                        if not have_played(player, opponent, match_history):
                            self.matches.append((player, opponent))
                            used.add(player)
                            used.add(opponent)
                            found = True
                            break
                    if not found:
                        success = False
                        break
                if success:
                    self.removed_player = removed_player
                    return
        else:
            self.matches = []
            sorted_players = self.generate_sorted_players(players_copy)
            used = set()
            success = True
            for i, (player, _) in enumerate(sorted_players):
                if player in used:
                    continue
                found = False
                for j in range(i + 1, len(sorted_players)):
                    opponent, _ = sorted_players[j]
                    if opponent in used:
                        continue
                    if not have_played(player, opponent, match_history):
                        self.matches.append((player, opponent))
                        used.add(player)
                        used.add(opponent)
                        found = True
                        break
                if not found:
                    success = False
                    break
            if success:
                self.removed_player = None
                return
        self.matches = []
        self.removed_player = None


def recreate_rounds(rounds_list):
    rounds = []
    for round in rounds_list:
        if round["type"] == "First Round":
            recreated_round = FirstRound(round["players"],
                                         round["matches"],
                                         round["finished"],
                                         round["start_date"],
                                         round["end_date"],
                                         round["removed_player"])
            rounds.append(recreated_round)
        elif round["type"] == "Subsequent Round":
            recreated_round = SubsequentRound(round["name"],
                                              round["players"],
                                              round["number"],
                                              round["matches"],
                                              round["finished"],
                                              round["start_date"],
                                              round["end_date"],
                                              round["removed_player"])
            rounds.append(recreated_round)
        else:
            raise "Wrong round type"
    return rounds


def update_points(result, match, tournament):
    for tournament_player in tournament.players_list:
        tp_player_id = tournament_player.player.chess_national_id
        m0_player_id = match[0].player.chess_national_id
        m1_player_id = match[1].player.chess_national_id
        if tp_player_id == m0_player_id:
            player1 = tournament_player
        if tp_player_id == m1_player_id:
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
    pair = (p1.tournament_id, p2.tournament_id)
    reverse_pair = (p2.tournament_id, p1.tournament_id)
    return pair in match_history or reverse_pair in match_history
