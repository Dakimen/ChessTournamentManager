from models.player_models import Player, TournamentPlayer
from models.round_models import FirstRound, SubsequentRound
from storage_choice import data_manager


class Tournament:
    """
    Represents a chess tournament, including metadata, player information,
    and a sequence of rounds.

    Initializes a tournament using provided tournament data and players, and
    handles the generation of rounds, match history tracking, and serialization.

    Args:
        tournament_data (dict): Dictionary containing tournament metadata.
        players (list): List of Player objects (for fresh tournaments) or tuples
            of serialized TournamentPlayer data (for restored tournaments).
        rounds (list, optional): Previously played rounds (for tournament recreation).
        current_round (int, optional): Current round number (1-based index).

    Attributes:
        name (str): The name of the tournament.
        place (str): The location where the tournament takes place.
        dates (str): The formatted date range of the tournament.
        description (str): A brief description of the tournament.
        number_of_rounds (int): Total number of rounds to be played.
        str_players (list): List of players represented as dictionaries.
        players_list (list): List of TournamentPlayer instances.
        rounds (list): List of Round instances (FirstRound or SubsequentRound).
        current_round (int): Current round number (1-based index).
        match_history (list): List of tuples representing past matchups.

    Methods:
        get_removed_list():
        Builds a list of players removed from previous rounds due to odd numbers.
        Returns:
            list: A list of TournamentPlayer instances that were removed from rounds.

        generate_round():
        Generates and appends the next round in the tournament, if the total number of rounds
        has not yet been reached.
        Creates a FirstRound if no rounds exist yet; otherwise creates a SubsequentRound using
        Swiss pairing logic, avoiding repeat matches and handling odd player counts.

        stringify_rounds():
        Converts all matches in each round into string format (for display or export).
        Returns:
            list: A list of stringified match lists for each round.

        get_current_round():
        Retrieves the current round object based on the current round number.
        Returns:
            Round: The current Round instance.

        save_tournament():
        Serializes and saves the tournament data to persistent storage via `data_manager`.
        The data saved includes metadata, players, and all rounds as dictionaries.

        get_match_history():
        Builds the match history by extracting player ID pairs from all previous rounds.
        This history is used to prevent repeated matchups in future rounds
    """
    def __init__(self, tournament_data, players, rounds=[], current_round=1):
        self.name = tournament_data["tournament_name"]
        self.place = tournament_data["tournament_place"]
        self.dates = (f"{tournament_data["tournament_beginning_date"]}"
                      " - "
                      f"{tournament_data["tournament_end_date"]}")
        self.description = tournament_data["tournament_description"]
        if tournament_data["number_of_rounds"] == "":
            self.number_of_rounds = 4
        else:
            self.number_of_rounds = int(tournament_data["number_of_rounds"])
        self.str_players = []
        self.players_list = []
        n = 0
        while n < len(players):
            if isinstance(players[n], Player):
                new_tournament_player = TournamentPlayer(players[n], n)
                self.players_list.append(new_tournament_player)
            else:
                new_tournament_player = TournamentPlayer(players[n][0],
                                                         players[n][1],
                                                         players[n][2])
                self.players_list.append(new_tournament_player)
            n += 1
        for each_player in self.players_list:
            new_str_player = each_player.to_dict()
            self.str_players.append(new_str_player)
        self.rounds = []
        self.current_round = current_round
        self.match_history = []
        if rounds != []:
            for round in rounds:
                self.rounds.append(round)

    def get_removed_list(self):
        """
        Builds a list of players removed from previous rounds due to odd numbers.

        Returns:
            list: A list of TournamentPlayer instances that were removed from rounds.
        """
        removed_list = []
        for round in self.rounds:
            for player in self.players_list:
                if isinstance(round.removed_player, int):
                    if player.tournament_id == round.removed_player:
                        removed_list.append(player)
                elif isinstance(round.removed_player, TournamentPlayer):
                    pl_tourn_id = player.tournament_id
                    if pl_tourn_id == round.removed_player.tournament_id:
                        removed_list.append(player)
                else:
                    raise ("removed_player is an incorrect instance "
                           f"{type(round.removed_player)}")
        return removed_list

    def generate_round(self):
        """
        Generates and appends the next round in the tournament, if the total number of rounds
        has not yet been reached.

        Creates a FirstRound if no rounds exist yet; otherwise creates a SubsequentRound using
        Swiss pairing logic, avoiding repeat matches and handling odd player counts.
        """
        if len(self.rounds) < self.number_of_rounds:
            if len(self.rounds) == 0:
                new_round = FirstRound(self.players_list)
                new_round.generate_matches()
                self.rounds.append(new_round)
            else:
                self.get_match_history()
                match_history = self.match_history
                removed_list = self.get_removed_list()
                n = len(self.rounds) + 1
                new_round = SubsequentRound(f"Round {n}",
                                            self.players_list, n)
                new_round.generate_matches(match_history, removed_list)
                self.rounds.append(new_round)
        else:
            return None

    def stringify_rounds(self):
        """
        Converts all matches in each round into string format (for display or export).

        Returns:
            list: A list of stringified match lists for each round.
        """
        stringified_rounds = []
        for round in self.rounds:
            round_strings = round.stringify_matches()
            stringified_rounds.append(round_strings)
        return stringified_rounds

    def get_current_round(self):
        """
        Retrieves the current round object based on the current round number.

        Returns:
            Round: The current Round instance.
        """
        number = self.current_round - 1
        current_round = self.rounds[number]
        return current_round

    def save_tournament(self):
        """
        Serializes and saves the tournament data to persistent storage via `data_manager`.

        The data saved includes metadata, players, and all rounds as dictionaries.
        """
        round_dict = []
        for round in self.rounds:
            round_dict.append(round.get_data())
        data_manager.save_tournament(
            self.name,
            self.place,
            self.dates,
            self.description,
            self.number_of_rounds,
            self.current_round,
            self.str_players,
            round_dict
            )

    def get_match_history(self):
        """
        Builds the match history by extracting player ID pairs from all previous rounds.

        This history is used to prevent repeated matchups in future rounds.
        """
        matches = []
        for round in self.rounds:
            for match in round.matches:
                match_tup = (match[0].tournament_id, match[1].tournament_id)
                matches.append(match_tup)
        self.match_history = matches
