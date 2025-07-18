from models.model import Player, check_chess_id_validity, list_all_players, sort_players_alphabetically
from views.main_view import player_addition_view, handle_false_id, display_list_of_players

def handle_add_new_player():
    new_player_data = player_addition_view()
    new_player = Player(new_player_data)
    list_of_all_players = list_all_players()
    all_player_ids = [player.get("chess_national_id") for player in list_of_all_players]
    if check_chess_id_validity(new_player.chess_national_id, all_player_ids) is False:
        while check_chess_id_validity(new_player.chess_national_id, all_player_ids) is False:
            new_player.chess_national_id = handle_false_id()
    new_player.save_player()

def get_all_players_alphabetically():
    players_unsorted = list_all_players()
    players_sorted = sort_players_alphabetically(players_unsorted)
    display_list_of_players(players_sorted)
