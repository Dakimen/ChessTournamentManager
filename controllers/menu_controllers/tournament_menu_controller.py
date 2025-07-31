from views.menu import Menu
from controllers.tournament_controllers.tournament_creation import (
     manage_create_tournament
     )
from controllers.menu_controllers.choice_of_ongoing import (
     ongoing_tournaments_list_menu
     )
from controllers.tournament_controllers.tournament_management import (
     list_all_tournaments, find_a_tournament
     )

TOURNAMENT_MENU_CHOICES = {
    "1": {"text": "Create new tournament",
          "key": "1", "action": manage_create_tournament},
    "2": {"text": "Manage ongoing tournaments",
          "key": "2", "action": ongoing_tournaments_list_menu},
    "3": {"text": "List all tournaments",
          "key": "3", "action": list_all_tournaments},
    "4": {"text": "Find a tournament",
          "key": "4", "action": find_a_tournament},
    "5": {"text": "Back to Main Menu",
          "key": "5", "action": None}
    }


def tournament_menu_controller():
    tournament_menu = Menu("Tournament menu", TOURNAMENT_MENU_CHOICES)
    decision = tournament_menu.display_menu()
    decision_text = TOURNAMENT_MENU_CHOICES[decision]["text"]
    if decision_text != "Back to Main Menu":
        while decision_text != "Back to Main Menu":
            TOURNAMENT_MENU_CHOICES[decision]["action"]()
            decision = tournament_menu.display_menu()
            decision_text = TOURNAMENT_MENU_CHOICES[decision]["text"]
    from controllers.menu_controllers.main_menu_controller import (
        main_menu_controller
        )
    return main_menu_controller()
