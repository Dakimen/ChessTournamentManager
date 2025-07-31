from models.player_models import (
    Player, check_chess_id_validity, list_all_players,
    sort_players_alphabetically
    )
from views.player_menu_views import (
    player_addition_view, handle_false_id, display_list_of_players
    )


def handle_add_new_player():
    new_player_data = player_addition_view()
    new_player = Player(new_player_data)
    list_of_all_players = list_all_players()
    all_player_ids = [
        player.get("chess_national_id")
        for player in list_of_all_players
        ]
    new_player_id = new_player.chess_national_id
    id_valid = check_chess_id_validity(new_player_id, all_player_ids)
    if id_valid is False:
        while id_valid is False:
            new_player.chess_national_id = handle_false_id()
            new_player_id = new_player.chess_national_id
            id_valid = check_chess_id_validity(new_player_id, all_player_ids)
    new_player.save_player()


def get_all_players_alphabetically():
    players_unsorted = list_all_players()
    players_unsort_obj = []
    for player in players_unsorted:
        obj_player = Player(player)
        players_unsort_obj.append(obj_player)
    players_sorted = sort_players_alphabetically(players_unsort_obj)
    display_list_of_players(players_sorted)
