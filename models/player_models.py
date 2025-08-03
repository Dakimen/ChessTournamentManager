from storage_choice import data_manager


class Player:
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
    def __init__(self, player: Player, tournament_id,
                 player_tournament_points=0):
        self.player = player
        self.tournament_points = player_tournament_points
        self.tournament_id = tournament_id

    def __eq__(self, other):
        if isinstance(other, TournamentPlayer):
            return self.tournament_id == other.tournament_id
        else:
            return False

    def __hash__(self):
        return hash(self.tournament_id)

    def __repr__(self):
        return f"{self.player.surname}"

    def get_player_score_list(self):
        player_score = [self.player.to_dict(), self.tournament_points]
        return player_score

    def to_dict(self):
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
