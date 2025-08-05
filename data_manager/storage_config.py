from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from abc import ABC, abstractmethod


class PrettyJSONStorage(JSONStorage):
    """Class modifying indent value of JSONStorage to 4 in order to make it prettier"""
    def __init__(self, *args, **kwargs):
        kwargs['indent'] = 4
        super().__init__(*args, **kwargs)


class DataManager(ABC):
    """
    Abstract Base Class for Data Managers, setting expected methods to be implemented.

    Abstract Methods:

    save_player(name, surname, date_of_birth, chess_national_id):
    Saves player to the database
    Args:
    name (string)
    surname (string)
    date_of_birth (string, in yyyy format)
    chess_national_id (string, in 'ID00000' format)

    list_all_players():
    Returns a list of all players stored in the database

    find_tournament(name, dates):
    Finds a tournament with a matching name and dates in the database.
    Args:
    name (string)
    dates (string, in 'dd/mm/yyyy - dd/mm/yyyy' format)

    get_all_tournaments():
    Retrieves a list of all tournaments stored in the database.

    mark_round_finished(current_round, tournament):
    Marks current round finished.
    Args:
    round (Round object to set as finished)
    tournament (Tournament object that contains this round)

    update_current_round(tournament):
    Updates tournament.current_round value in the database.
    Args:
    tournament (Tournament object)

    update_player_points_in_db(tournament):
    Updates player points in the database.
    Args:
    tournament (Tournament object with modified player points)

    get_tournament_id_in_db(tournament):
    Finds tournament_id based on the name of a given tournament.
    Args:
    tournament (Tournament object)

    check_if_in_db(new_player):
    Checks if a player with a corresponding national chess id exists in the database.
    Args:
    new_player (Player object)
    Returns a boolean.

    get_player_from_db(player_data):
    Gets all the data of a given player from the database
    Args:
    player_data (dict, containing a chess_national_id string in 'ID00000' format)
    Returns a dict containing all the player's data.

    save_tournament(
        name, place,
        dates, description,
        number_of_rounds, current_round,
        str_players, round_dict
    ):
    Saves a new tournament to the database.
    Args:
    name (string)
    place (string)
    dates (string in 'dd/mm/yyyy - dd/mm/yyyy' format)
    description (string)
    number_of_rounds (string containing a number)
    current_round (string containing the number of the currently played round)
    "str_player" (list containing player data dictionaries)
    "round_dict" (list containing round data dictionaries)
    """
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def save_player(self, name, surname, date_of_birth, chess_national_id):
        """
        Saves player to the database
        Subclasses must implement this method.
        Args:
        name (string)
        surname (string)
        date_of_birth (string, in yyyy format)
        chess_national_id (string, in 'ID00000' format)
        """
        pass

    @abstractmethod
    def list_all_players(self):
        """
        Returns a list of all players stored in the database.
        Subclasses must implement this method.
        """
        pass

    @abstractmethod
    def find_tournament(self, name, dates):
        """
        Finds a tournament with a matching name and dates in the database.
        Subclasses must implement this method.
        Args:
        name (string)
        dates (string, in 'dd/mm/yyyy - dd/mm/yyyy' format)
        """
        pass

    @abstractmethod
    def get_all_tournaments(self):
        """
        Retrieves a list of all tournaments stored in the database.
        Subclasses must implement this method.
        """
        pass

    @abstractmethod
    def mark_round_finished(self, current_round, tournament):
        """
        Marks current round finished.
        Subclasses must implement this method.
        Args:
        round (Round object to set as finished)
        tournament (Tournament object that contains this round)
        """
        pass

    @abstractmethod
    def update_current_round(self, tournament):
        """
        Updates tournament.current_round value in the database.
        Subclasses must implement this method.
        Args:
        tournament (Tournament object)
        """
        pass

    @abstractmethod
    def update_player_points_in_db(self, tournament):
        """
        Updates player points in the database.
        Subclasses must implement this method.
        Args:
        tournament (Tournament object with modified player points)
        """
        pass

    @abstractmethod
    def get_tournament_id_in_db(self, tournament):
        """
        Finds tournament_id based on the name of a given tournament.
        Subclasses must implement this method.
        Args:
        tournament (Tournament object)
        """
        pass

    @abstractmethod
    def check_if_in_db(self, new_player):
        """
        Checks if a player with a corresponding national chess id exists in the database.
        Subclasses must implement this method.
        Args:
        new_player (Player object)
        Returns a boolean.
        """
        pass

    @abstractmethod
    def get_player_from_db(self, player_data):
        """
        Gets all the data of a given player from the database.
        Subclasses must implement this method.
        Args:
        player_data (dict, containing a chess_national_id string in 'ID00000' format)
        Returns a dict containing all the player's data.
        """
        pass

    @abstractmethod
    def save_tournament(
        self,
        name,
        place,
        dates,
        description,
        number_of_rounds,
        current_round,
        str_players,
        round_dict
    ):
        """
        Saves a new tournament to the database.
        Subclasses must implement this method.
        Args:
        name (string)
        place (string)
        dates (string in 'dd/mm/yyyy - dd/mm/yyyy' format)
        description (string)number_of_rounds (string containing a number)
        current_round (string containing the number of the currently played round)
        "str_player" (list containing player data dictionaries)
        "round_dict" (list containing round data dictionaries)
        """
        pass


class DataManagerTinyDB(DataManager):
    """
    Data Manager class for TinyDB database management.

    Attributes:
    tournament_db (TinyDB object connected to tournament_database.json)
    player_db (TinyDB object connected to player_database.json)

    Methods:

    save_player(name, surname, date_of_birth, chess_national_id):
    Saves player to the database
    Args:
    name (string)
    surname (string)
    date_of_birth (string, in yyyy format)
    chess_national_id (string, in 'ID00000' format)

    list_all_players():
    Returns a list of all players stored in the database

    find_tournament(name, dates):
    Finds a tournament with a matching name and dates in the database.
    Args:
    name (string)
    dates (string, in 'dd/mm/yyyy - dd/mm/yyyy' format)

    get_all_tournaments():
    Retrieves a list of all tournaments stored in the database.

    mark_round_finished(current_round, tournament):
    Marks current round finished.
    Args:
    round (Round object to set as finished)
    tournament (Tournament object that contains this round)

    update_current_round(tournament):
    Updates tournament.current_round value in the database.
    Args:
    tournament (Tournament object)

    update_player_points_in_db(tournament):
    Updates player points in the database.
    Args:
    tournament (Tournament object with modified player points)

    get_tournament_id_in_db(tournament):
    Finds tournament_id based on the name of a given tournament.
    Args:
    tournament (Tournament object)

    check_if_in_db(new_player):
    Checks if a player with a corresponding national chess id exists in the database.
    Args:
    new_player (Player object)
    Returns a boolean.

    get_player_from_db(player_data):
    Gets all the data of a given player from the database
    Args:
    player_data (dict, containing a chess_national_id string in 'ID00000' format)
    Returns a dict containing all the player's data.

    save_tournament(
        name, place,
        dates, description,
        number_of_rounds, current_round,
        str_players, round_dict
    ):
    Saves a new tournament to the database.
    Args:
    name (string)
    place (string)
    dates (string in 'dd/mm/yyyy - dd/mm/yyyy' format)
    description (string)
    number_of_rounds (string containing a number)
    current_round (string containing the number of the currently played round)
    "str_player" (list containing player data dictionaries)
    "round_dict" (list containing round data dictionaries)
    """
    def __init__(self):
        self.player_db = TinyDB("player_database.json", storage=PrettyJSONStorage)
        self.tournament_db = TinyDB("tournament_database.json", storage=PrettyJSONStorage)

    def save_player(self, name, surname, date_of_birth, chess_national_id):
        """
        Saves player to the TinyDB database
        Args:
        name (string)
        surname (string)
        date_of_birth (string, in yyyy format)
        chess_national_id (string, in 'ID00000' format)
        """
        self.player_db.insert({
            "player_name": name,
            "player_surname": surname,
            "date_of_birth": date_of_birth,
            "chess_national_id": chess_national_id
            })
        return True

    def list_all_players(self):
        """
        Returns a list of all players stored in the TinyDB database.
        """
        list_of_all_players = self.player_db.all()
        return list_of_all_players

    def find_tournament(self, name, dates):
        """
        Finds a tournament with a matching name and dates in the TinyDB database.
        Args:
        name (string)
        dates (string, in 'dd/mm/yyyy - dd/mm/yyyy' format)
        """
        tournament = Query()
        found_tournament_by_name = self.tournament_db.search(tournament.name == name)
        tournaments_during = self.tournament_db.search(tournament.dates == dates)
        for tournament in found_tournament_by_name:
            if tournament in tournaments_during:
                return tournament
        else:
            return None

    def get_all_tournaments(self):
        """
        Retrieves a list of all tournaments stored in the TinyDB database.
        """
        all_tournaments = self.tournament_db.all()
        return all_tournaments

    def mark_round_finished(self, current_round, tournament):
        """
        Marks current round finished in the TinyDB database.
        Args:
        round (Round object to set as finished)
        tournament (Tournament object that contains this round)
        """
        current_round.finish_round()
        tournament_id = self.get_tournament_id_in_db(tournament)
        updated_rounds = []
        for round in tournament.rounds:
            upd_round = round.get_data()
            updated_rounds.append(upd_round)
        self.tournament_db.update({"rounds": updated_rounds},
                                  doc_ids=[tournament_id])

    def update_current_round(self, tournament):
        """
        Updates tournament.current_round value in the TinyDB database.
        Args:
        tournament (Tournament object)
        """
        tournament_id = self.get_tournament_id_in_db(tournament)
        if tournament.current_round != tournament.number_of_rounds:
            new_current_round = tournament.current_round + 1
            self.tournament_db.update({"current_round": new_current_round}, doc_ids=[tournament_id])

    def update_player_points_in_db(self, tournament):
        """
        Updates player points in the database.
        Args:
        tournament (Tournament object with modified player points)
        """
        tournament_id = self.get_tournament_id_in_db(tournament)
        tournament.str_players = []
        for player in tournament.players_list:
            str_player = player.to_dict()
            tournament.str_players.append(str_player)
        self.tournament_db.update({"players_list_raw": tournament.str_players},
                                  doc_ids=[tournament_id])

    def get_tournament_id_in_db(self, tournament):
        """
        Finds tournament_id based on the name of a given tournament in the TinyDB database.
        Args:
        tournament (Tournament object)
        """
        t_in_db = Query()
        tournament_doc = self.tournament_db.search(t_in_db.name == tournament.name)[0]
        tournament_id = tournament_doc.doc_id
        return tournament_id

    def check_if_in_db(self, new_player):
        """
        Checks if a player with a corresponding national chess id exists in the database.
        Args:
        new_player (Player object)
        Returns a boolean.
        """
        db_player = Query()
        return bool(self.player_db.search(
            (db_player.chess_national_id == new_player["chess_national_id"])
        ))

    def get_player_from_db(self, player_data):
        """
        Gets all the data of a given player from the database.
        Args:
        player_data (dict, containing a chess_national_id string in 'ID00000' format)
        Returns a dict containing all the player's data.
        """
        db_player = Query()
        player_c_nd = f"{player_data['chess_national_id']}"
        player_fnd = self.player_db.search(db_player.chess_national_id == player_c_nd)
        return player_fnd[0]

    def save_tournament(
        self,
        name,
        place,
        dates,
        description,
        number_of_rounds,
        current_round,
        str_players,
        round_dict
    ):
        """
        Saves a new tournament to the database.
        Subclasses must implement this method.
        Args:
        name (string)
        place (string)
        dates (string in 'dd/mm/yyyy - dd/mm/yyyy' format)
        description (string)number_of_rounds (string containing a number)
        current_round (string containing the number of the currently played round)
        "str_player" (list containing player data dictionaries)
        "round_dict" (list containing round data dictionaries)
        """
        self.tournament_db.insert({
            "name": name,
            "place": place,
            "dates": dates,
            "description": description,
            "number_of_rounds": number_of_rounds,
            "current_round": current_round,
            "players_list_raw": str_players,
            "rounds": round_dict
        })
