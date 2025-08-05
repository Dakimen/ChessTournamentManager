from data_manager.storage_choice import data_manager


class Player:
    """
    Player class handling basic, non-tournament specific player information.

    Requires a player dictionary to instantiate, dictionary must contain:
        'player_name'
        'player_surname'
        'date_of_birth'
        'chess_national_id'

    Attributes:
        name (string): contains player's name
        surname (string): contains player's surname
        date_of_birth (string): contains player's date of birth in yyyy format
        chess_national_id (string): contains player's national chess id in ID00000 format

    Methods:
        save_player(): Saves player to the database
        to_dict(): Creates a dictionary containing all the player attributes
    """
    def __init__(self, player_info):
        self.name = player_info["player_name"]
        self.surname = player_info["player_surname"]
        self.date_of_birth = player_info["date_of_birth"]
        self.chess_national_id = player_info["chess_national_id"]

    def save_player(self):
        """Saves player to the database"""
        data_manager.save_player(
            self.name,
            self.surname,
            self.date_of_birth,
            self.chess_national_id
            )
        return True

    def to_dict(self):
        """Creates a dictionary containing all the player attributes"""
        self_dict = {
            "player_name": self.name,
            "player_surname": self.surname,
            "date_of_birth": self.date_of_birth,
            "chess_national_id": self.chess_national_id
        }
        return self_dict


class TournamentPlayer:
    """
    Represents a player participating in a specific tournament, along with their tournament-specific data.

    This class wraps a Player object and adds tournament-specific attributes like points and ID.
    It also implements comparison and hashing based on the tournament ID, which allows instances
    to be used in sets and as dictionary keys.

    Attributes:
        player (Player): The player object containing personal data.
        tournament_points (int): The number of points this player has in the tournament.
        tournament_id (string): The identifier of the tournament this player is participating in.

    Methods:
        __eq__(other):
            Compares two TournamentPlayer instances based on tournament ID.

        __hash__():
            Returns a hash based on the tournament ID for use in sets and dicts.

        __repr__():
            Returns a string representation of the player, showing only the surname.

        get_player_score_list():
            Returns a list containing the player's data and their tournament points.

        to_dict():
            Serializes the TournamentPlayer object into a dictionary format,
            including embedded player data and tournament-specific fields.
    """
    def __init__(self, player: Player, tournament_id,
                 player_tournament_points=0):
        self.player = player
        self.tournament_points = player_tournament_points
        self.tournament_id = tournament_id

    def __eq__(self, other):
        """Compares two TournamentPlayer instances based on tournament ID."""
        if isinstance(other, TournamentPlayer):
            return self.tournament_id == other.tournament_id
        else:
            return False

    def __hash__(self):
        """Returns a hash based on the tournament ID."""
        return hash(self.tournament_id)

    def __repr__(self):
        """Returns a string representation of the player showing only the surname and national chess id"""
        return f"{self.player.surname}, f{self.player.chess_national_id}"

    def get_player_score_list(self):
        """Returns a list containing the player's data dictionary and their tournament points."""
        player_score = [self.player.to_dict(), self.tournament_points]
        return player_score

    def to_dict(self):
        """Serializes the TournamentPlayer object into a dictionary format,
           including embedded player data and tournament-specific fields."""
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
