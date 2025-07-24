from models.tournament_models import get_all_tournaments
from views.tournament_views import show_ongoing_tournaments
from menu_controllers.ongoing_tourn_menu import ongoing_tournament_menu

def ongoing_tournaments_list_menu():
    all_tournaments = get_all_tournaments()
    ongoing_tournaments = []
    for tournament in all_tournaments:
        unfinished_rounds = []
        for round in tournament["rounds"]:
            if round["finished"] is False:
                unfinished_rounds.append(round)
        if unfinished_rounds != []:
            ongoing_tournaments.append(tournament)
    ongoing_tournaments_info = []
    key = 1
    for tournament in ongoing_tournaments:
        ongoing_dict = {"name": tournament["name"], "dates": tournament["dates"], "key": key}
        ongoing_tournaments_info.append(ongoing_dict)
        key += 1
    choice = show_ongoing_tournaments(ongoing_tournaments_info)
    if choice == None:
        return None
    if int(choice) == ongoing_tournaments_info[-1]["key"] + 1:
        from menu_controllers.tournament_menu_controller import tournament_menu_controller
        return tournament_menu_controller()
    chosen_tournament = []
    for tournament in ongoing_tournaments_info:
        if tournament["key"] == int(choice):
            chosen_tournament.append(tournament)
    return ongoing_tournament_menu(chosen_tournament)
    
    


