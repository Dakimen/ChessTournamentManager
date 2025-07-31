from models.tournament_models import find_tournament
from models.tournament_models import (
    update_player_points_in_db, mark_round_finished
    )
from models.player_models import get_participating_players_from_data
from models.round_models import recreate_rounds, update_points
from views.tournament_views import (
    show_current_round_info, get_round_results, display_leaderboard
    )
from controllers.player_controllers.player_controller import (
    sort_players_alphabetically
    )
from views.player_menu_views import display_list_of_players
from views.round_views import display_round_history
from controllers.tournament_controllers.tournament_management import (
    recreate_tournament
    )


def manage_current_round(tournament_base_info):
    recreated_tournament = recreate_tournament(tournament_base_info[0])
    current_round = recreated_tournament.get_current_round()
    show_current_round_info(current_round.matches)
    result_list = get_round_results(current_round.matches)
    if result_list is None:
        return None
    if result_list is not None:
        n = 0
        while n < len(result_list):
            update_points(result_list[n],
                          current_round.matches[n],
                          recreated_tournament)
            n += 1
    update_player_points_in_db(recreated_tournament)
    recreated_tournament.generate_round()
    mark_round_finished(current_round, recreated_tournament)


def show_players_alphabetic(tournament):
    found_data = find_tournament(tournament[0]["name"],
                                 tournament[0]["dates"])
    participants = get_participating_players_from_data(found_data)
    player_objects = []
    for participant in participants:
        player_objects.append(participant[0])
    sorted_players = sort_players_alphabetically(player_objects)
    display_list_of_players(sorted_players)


def show_leaderboard(tournament):
    found_data = find_tournament(tournament[0]["name"],
                                 tournament[0]["dates"])
    participants = get_participating_players_from_data(found_data)
    players_and_points = []
    for participant in participants:
        player_and_points = tuple()
        player_and_points = (participant[0], participant[2])
        players_and_points.append(player_and_points)
    players_and_points_sorted = sorted(players_and_points,
                                       key=lambda player: player[1],
                                       reverse=True)
    display_leaderboard(players_and_points_sorted)


def show_round_history(tournament):
    found_data = find_tournament(tournament[0]["name"],
                                 tournament[0]["dates"])
    found_rounds = recreate_rounds(found_data["rounds"])
    for round in found_rounds:
        round.recreate_matches()
    for round in found_rounds:
        round.recreate_players()
    display_round_history(found_rounds)
