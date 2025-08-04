from datetime import datetime
import random
from models.player_models import Player, TournamentPlayer, data_manager
from models.round_utility import have_played


class Round:
    """
    Represents a single round in a tournament, including its players, matches, and metadata.

    This class provides methods for generating and restoring matches, recording round data,
    and serializing it for storage.

    Attributes:
        name (str): Name of the round.
        number (int): Round number.
        start_date (str): Start date of the round.
        end_date (str): End date of the round (recorded when the round finishes).
        players (list): List of TournamentPlayer instances participating in the round.
        matches (list): List of match tuples, each containing two TournamentPlayer instances.
        finished (bool): Whether the round is finished.
        type (str): Type of the round (e.g., "First", "Subsequent").
        removed_player (TournamentPlayer or int): Player removed due to odd number of participants.

    Methods:
        generate_matches():
            Abstract method to generate matches for the round.
            Must be implemented by subclasses.

        finish_round():
            Marks the round as finished and records the current timestamp as the end date.

        stringify_matches():
            Converts the list of matches into readable string representations for display.

        get_data():
            Serializes the round into a dictionary, including players, matches,
            timestamps, and metadata for storage or reconstruction.

        recreate_matches():
            Reconstructs the match objects using stored match data and players from the database.

        recreate_players():
            Recreates the TournamentPlayer objects from serialized player dictionaries.

        recreate_removed_player():
            Resolves the removed_player ID by matching it to the correct TournamentPlayer
            instance in the players list.
    """
    def generate_matches(self):
        """Generates matches"""
        raise NotImplementedError(
            "This function must be implemented in the subclasses"
            )

    def finish_round(self):
        """Marks round finished and records the time of this operation."""
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
        """Creates a dictionary containing all the data contained in the Round class."""
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
            string_player = player.to_dict()
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
        """Recreates TournamentPlayer objects within matches from matches attribute of this class instance.
           Takes no arguments."""
        matches = []
        for match in self.matches:
            player1_info = data_manager.get_player_from_db(match[0][0])
            player2_info = data_manager.get_player_from_db(match[1][0])
            player1_obj = Player(player1_info)
            player2_obj = Player(player2_info)
            tourn_player1 = TournamentPlayer(player1_obj,
                                             match[0][1],
                                             match[0][2])
            tourn_player2 = TournamentPlayer(player2_obj,
                                             match[1][1],
                                             match[1][2])
            new_match = (tourn_player1, tourn_player2)
            matches.append(new_match)
        self.matches = matches

    def recreate_players(self):
        """Recreates TournamentPlayer objects in self.players.
           Takes no argument"""
        players = []
        for player in self.players:
            player_obj = Player(player["player"])
            t_player = TournamentPlayer(player_obj,
                                        player["tournament_id"],
                                        player["tournament_points"])
            players.append(t_player)
        self.players = players

    def recreate_removed_player(self):
        """Gets removed player in cases of an odd number of players.
           Matches id in self.players to self.removed_player
           Takes no argument"""
        for player in self.players:
            if player.tournament_id == self.removed_player:
                self.removed_player = player


class FirstRound(Round):
    """
    Represents the first round of a tournament.

    Inherits from the Round base class and implements match generation logic specific to
    the first round (randomized pairing). Handles odd numbers of players by removing
    a designated player (with tournament_id == 0).

    Attributes:
        name (str): Name of the round ("Round 1").
        players (list): List of TournamentPlayer instances participating in the round.
        number (int): Round number (always 1 for the first round).
        finished (bool): Whether the round has been marked as finished.
        start_date (str): Timestamp when the round started.
        end_date (str or int): Timestamp when the round ended or 0 if not finished.
        matches (list): List of randomly generated match tuples.
        type (str): Type of round ("First Round").
        removed_player (TournamentPlayer or None):
        The player removed from the round if the number of participants is odd.

    Methods:
        generate_matches():
            Generates matches by randomly pairing players.
            If the number of players is odd, removes the player with tournament_id == 0.
    """
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
        """Generates matches by randomly pairing players.
           If the number of players is odd, removes the player with tournament_id == 0."""
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
    """
    Represents a tournament round occurring after the first one.

    This class implements match generation using a Swiss-style pairing system, where players
    are sorted by score and matched against opponents they haven't faced yet. In case of
    an odd number of participants, one player is removed from the round.

    Attributes:
        name (str): Name of the round (e.g., "Round 2").
        players (list): List of TournamentPlayer instances in the round.
        number (int): Round number.
        finished (bool): Indicates whether the round has concluded.
        start_date (str): Timestamp when the round started.
        end_date (str or int): Timestamp when the round ended or 0 if unfinished.
        matches (list): List of tuples of matched TournamentPlayer instances.
        type (str): Type of round ("Subsequent Round").
        removed_player (TournamentPlayer or None): Player removed in case of odd number of participants.

    Methods:
        generate_sorted_players(players_copy):
            Takes a list of TournamentPlayer instances and returns a list of tuples
            (player, score), sorted by descending score.

        generate_matches(match_history, removed_list):
            Generates matches for the round using Swiss-style pairing:
            - Sorts players by score
            - Ensures no repeated matchups from previous rounds
            - Handles odd-numbered player lists by removing an available player not in `removed_list`
    """
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
        """Takes a list of TournamentPlayer instances and returns a list of tuples
           (player, score), sorted by descending score."""
        players_with_points = []
        self.matches = []
        for player in players_copy:
            player_with_points = (player, player.tournament_points)
            players_with_points.append(player_with_points)
        sorted_players = sorted(players_with_points, key=lambda x: x[1],
                                reverse=True)
        return sorted_players

    def generate_matches(self, match_history, removed_list):
        """Generates matches for the round using Swiss-style pairing:
            - Sorts players by score
            - Ensures no repeated matchups from previous rounds
            - Handles odd-numbered player lists by removing an available player not in 'removed_list'"""
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
    """Recreates rounds of both FirstRound and Subsequent Round types.
       Arguments:
           List of round dictionaries, containing:
               'name' (str): Name of the round (e.g., 'Round 2').
               'players' (list): List of TournamentPlayer instances in the round.
               'number' (int): Round number.
               'finished' (bool): Indicates whether the round has concluded.
               'start_date' (str): Timestamp when the round started.
               'end_date' (str or int): Timestamp when the round ended or 0 if unfinished.
               'matches' (list): List of tuples of matched TournamentPlayer instances.
               'type' (str): Type of round ('First Round' or 'Subsequent Round').
               removed_player (TournamentPlayer or None): Player removed in case of odd number of participants."""
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
