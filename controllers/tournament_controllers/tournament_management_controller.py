from models.tournament_models import get_all_tournaments, find_tournament
from controllers.tournament_controllers.round_controller import recreate_rounds, get_participating_players_from_data
from models.tournament_models import Tournament, recreate_tournament_input, find_tournament
from views.tournament_views import display_all_tournaments, find_tournament_input, tournament_not_found

def recreate_tournament(tournament_base_info):
    found_data = find_tournament(tournament_base_info["name"], tournament_base_info["dates"])
    if found_data == None:
        tournament_not_found()
        return None
    tourn_input = recreate_tournament_input(found_data)
    participants = get_participating_players_from_data(found_data)
    found_rounds = recreate_rounds(found_data["rounds"])
    for round in found_rounds:
        round.recreate_matches()
    for round in found_rounds:
        round.recreate_players()
    recreated_tournament = Tournament(tourn_input, participants, found_rounds)
    return recreated_tournament

def list_all_tournaments():
    tournaments = get_all_tournaments()
    recreated_tournaments = []
    for tournament in tournaments:
        recreated_tournament = recreate_tournament(tournament)
        if recreated_tournament == None:
            return None
        recreated_tournaments.append(recreated_tournament)
    display_all_tournaments(recreated_tournaments)

def find_a_tournament():
    name_and_dates = find_tournament_input()
    tournament_data = {"name": name_and_dates[0], "dates": name_and_dates[1]}
    recreated_tournament = recreate_tournament(tournament_data)
    if recreated_tournament == None:
        return None
    tournaments = []
    tournaments.append(recreated_tournament)
    display_all_tournaments(tournaments)
