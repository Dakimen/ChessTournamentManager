from views.menu import Menu
from controllers.tournament_controllers.round_controller import manage_current_round, show_leaderboard 
from controllers.tournament_controllers.round_controller import show_round_history, show_players_alphabetic

UNFINISHED_TOURNAMENT_MENU = {
    "1": {"text": "Manage current round", "key": "1", "action": manage_current_round},
    "2": {"text": "Show leaderboard", "key": "2", "action": show_leaderboard},
    "3": {"text": "List all players alphabetically", "key": "3", "action": show_players_alphabetic},
    "4": {"text": "Show round history", "key": "4", "action": show_round_history},
    "5": {"text": "Back to previous menu", "key": "5", "action": None}
}

def ongoing_tournament_menu(chosen_tournament):
    tourn_management_menu = Menu(f"{chosen_tournament[0]["name"]} menu", UNFINISHED_TOURNAMENT_MENU)
    choice = tourn_management_menu.display_menu()
    if UNFINISHED_TOURNAMENT_MENU[choice]["text"] != "Back to previous menu":
        while UNFINISHED_TOURNAMENT_MENU[choice]["text"] != "Back to previous menu":
            UNFINISHED_TOURNAMENT_MENU[choice]["action"](chosen_tournament)
            choice = tourn_management_menu.display_menu()
    else:
        from controllers.menu_controllers.choice_of_ongoing import ongoing_tournaments_list_menu
        return ongoing_tournaments_list_menu()