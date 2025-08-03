from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from abc import ABC, abstractmethod


class PrettyJSONStorage(JSONStorage):
    def __init__(self, *args, **kwargs):
        kwargs['indent'] = 4
        super().__init__(*args, **kwargs)


class DataManager(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def save_player(self, name, surname, date_of_birth, chess_national_id):
        pass

    @abstractmethod
    def list_all_players(self):
        pass

    @abstractmethod
    def find_tournament(self, name, dates):
        pass

    @abstractmethod
    def get_all_tournaments(self):
        pass

    @abstractmethod
    def mark_round_finished(self, current_round, tournament):
        pass

    @abstractmethod
    def update_current_round(self, tournament):
        pass

    @abstractmethod
    def update_player_points_in_db(self, tournament):
        pass

    @abstractmethod
    def get_tournament_id_in_db(self, tournament):
        pass

    @abstractmethod
    def check_if_in_db(self, new_player):
        pass

    @abstractmethod
    def get_player_from_db(self, player_data):
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
        pass


class DataManagerTinyDB(DataManager):
    def __init__(self):
        self.player_db = TinyDB("player_database.json", storage=PrettyJSONStorage)
        self.tournament_db = TinyDB("tournament_database.json", storage=PrettyJSONStorage)

    def save_player(self, name, surname, date_of_birth, chess_national_id):
        """Saves player to the database"""
        self.player_db.insert({
            "player_name": name,
            "player_surname": surname,
            "date_of_birth": date_of_birth,
            "chess_national_id": chess_national_id
            })
        return True

    def list_all_players(self):
        """Returns a list of all players stored in the tinyDB database"""
        list_of_all_players = self.player_db.all()
        return list_of_all_players

    def find_tournament(self, name, dates):
        """Finds tournaments with a corresponding name during a corresponding period in tinyDB database"""
        tournament = Query()
        found_tournament_by_name = self.tournament_db.search(tournament.name == name)
        tournaments_during = self.tournament_db.search(tournament.dates == dates)
        for tournament in found_tournament_by_name:
            if tournament in tournaments_during:
                return tournament
        else:
            return None

    def get_all_tournaments(self):
        """Returns a list of all tournaments in tinyDB database"""
        all_tournaments = self.tournament_db.all()
        return all_tournaments

    def mark_round_finished(self, current_round, tournament):
        """Marks current_round finished"""
        current_round.finish_round()
        tournament_id = self.get_tournament_id_in_db(tournament)
        updated_rounds = []
        for round in tournament.rounds:
            upd_round = round.get_data()
            updated_rounds.append(upd_round)
        self.tournament_db.update({"rounds": updated_rounds},
                                  doc_ids=[tournament_id])
        
    def update_current_round(self, tournament):
        """updates tournament.current_round in tinyDB"""
        tournament_id = self.get_tournament_id_in_db(tournament)
        new_current_round = tournament.current_round + 1
        self.tournament_db.update({"current_round": new_current_round},
                                  doc_ids=[tournament_id])

    def update_player_points_in_db(self, tournament):
        """Updates player point in tinyDB"""
        tournament_id = self.get_tournament_id_in_db(tournament)
        tournament.str_players = []
        for player in tournament.players_list:
            str_player = player.to_dict()
            tournament.str_players.append(str_player)
        self.tournament_db.update({"players_list_raw": tournament.str_players},
                                  doc_ids=[tournament_id])

    def get_tournament_id_in_db(self, tournament):
        """Finds tournament_id based on the name of a given tournament"""
        t_in_db = Query()
        tournament_doc = self.tournament_db.search(t_in_db.name == tournament.name)[0]
        tournament_id = tournament_doc.doc_id
        return tournament_id

    def check_if_in_db(self, new_player):
        db_player = Query()
        return bool(self.player_db.search(
            (db_player.chess_national_id == new_player["chess_national_id"])
        ))

    def get_player_from_db(self, player_data):
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
