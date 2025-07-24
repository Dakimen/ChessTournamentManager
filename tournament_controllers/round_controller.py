from models.tournament_models import find_tournament, recreate_tournament_input, Tournament, update_player_points_in_db, mark_round_finished
from models.player_models import get_participating_players_from_data
from models.round_models import recreate_rounds, update_points
from views.tournament_views import show_current_round_info, get_round_results

def manage_current_round(tournament_base_info):
    found_data = find_tournament(tournament_base_info[0]["name"], tournament_base_info[0]["dates"])
    tourn_input = recreate_tournament_input(found_data)
    participants = get_participating_players_from_data(found_data)
    found_rounds = recreate_rounds(found_data["rounds"])
    recreated_tournament = Tournament(tourn_input, participants, found_rounds)
    current_round = recreated_tournament.get_current_round()
    show_current_round_info(current_round.matches)
    result_list = get_round_results(current_round.matches)
    if result_list == None:
        return None
    if result_list != None:
        n = 0
        while n < len(result_list):
            update_points(result_list[n], current_round.matches[n], recreated_tournament)
            n += 1
    update_player_points_in_db(recreated_tournament)
    mark_round_finished(current_round, recreated_tournament)
    #Next we generate a new round
    


def show_leaderboard(tournament):
    pass

def show_round_history(tournament):
    pass