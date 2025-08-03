from models.player_models import Player
from storage_choice import data_manager
from models.player_utility import check_chess_id_validity, sort_players_alphabetically


class PlayerController:
    def __init__(self, player_view):
        self.player_view = player_view

    def handle_add_new_player(self):
        new_player_data = self.player_view.player_addition_view()
        new_player = Player(new_player_data)
        list_of_all_players = data_manager.list_all_players()
        all_player_ids = [
            player.get("chess_national_id")
            for player in list_of_all_players
            ]
        new_player_id = new_player.chess_national_id
        id_valid = check_chess_id_validity(new_player_id, all_player_ids)
        if id_valid is False:
            while id_valid is False:
                new_player.chess_national_id = self.player_view.handle_false_id()
                new_player_id = new_player.chess_national_id
                id_valid = check_chess_id_validity(new_player_id, all_player_ids)
        new_player.save_player()

    def get_all_players_alphabetically(self):
        players_unsorted = data_manager.list_all_players()
        players_unsort_obj = []
        for player in players_unsorted:
            obj_player = Player(player)
            players_unsort_obj.append(obj_player)
        players_sorted = sort_players_alphabetically(players_unsort_obj)
        self.player_view.display_list_of_players(players_sorted)
