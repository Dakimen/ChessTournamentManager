import re
from models.player_models import Player


def check_chess_id_validity(new_player_id, all_chess_ids):
    pattern = r"^[A-Z]{2}\d{5}$"
    if new_player_id in all_chess_ids:
        return False
    if re.match(pattern, new_player_id) is None:
        return False
    return True


def sort_players_alphabetically(players_to_sort):
    sorted_players = sorted(players_to_sort, key=lambda p: p.surname)
    return sorted_players


def get_participating_players_from_data(tourn_data):
    player_tuples = []
    for player in tourn_data["players_list_raw"]:
        player_obj = Player(player["player"])
        player_tournament_id = player["tournament_id"]
        player_points = player["tournament_points"]
        player_tuple = (player_obj, player_tournament_id, player_points)
        player_tuples.append(player_tuple)
    return player_tuples
