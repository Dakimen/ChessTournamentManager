from views.menu import Menu

UNFINISHED_TOURNAMENT_MENU = {
    "1": {"text": "Manage current round", "key": "1", "action": None},
    "2": {"text": "Show leaderboard", "key": "2", "action": None},
    "3": {"text": "Show round history", "key": "3", "action": None},
    "4": {"text": "Back to previous menu", "key": "4", "action": None}
}

def ongoing_tournament_menu(chosen_tournament):
    tourn_management_menu = Menu(f"{chosen_tournament[0]["name"]} menu", UNFINISHED_TOURNAMENT_MENU)
    choice = tourn_management_menu.display_menu()
    if UNFINISHED_TOURNAMENT_MENU[choice]["text"] != "Back to previous menu":
        while UNFINISHED_TOURNAMENT_MENU[choice]["text"] != "Back to previous menu":
            UNFINISHED_TOURNAMENT_MENU[choice]["action"]()
            choice = tourn_management_menu.display_menu()
    else:
        from menu_controllers.choice_of_ongoing import ongoing_tournaments_list_menu
        return ongoing_tournaments_list_menu()