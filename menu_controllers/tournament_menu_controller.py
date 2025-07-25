from views.menu import Menu
from tournament_controllers.tournament_creation_controller import manage_create_tournament
from menu_controllers.choice_of_ongoing import ongoing_tournaments_list_menu

TOURNAMENT_MENU_CHOICES = {
    "1": {"text": "Create new tournament", "key": "1", "action": manage_create_tournament}, 
    "2": {"text": "Manage ongoing tournaments", "key": "2", "action": ongoing_tournaments_list_menu},
    "3": {"text": "List all tournaments", "key": "3", "action": None},
    "4": {"text": "Find a tournament", "key": "4", "action": None},
    "5": {"text": "Back to Main Menu", "key": "5", "action": None}
    }

def tournament_menu_controller():
      tournament_menu = Menu("Tournament menu", TOURNAMENT_MENU_CHOICES)
      decision_tournament_menu = tournament_menu.display_menu()
      if TOURNAMENT_MENU_CHOICES[decision_tournament_menu]["text"] != "Back to Main Menu":
          while TOURNAMENT_MENU_CHOICES[decision_tournament_menu]["text"] != "Back to Main Menu":
              TOURNAMENT_MENU_CHOICES[decision_tournament_menu]["action"]()
              decision_tournament_menu = tournament_menu.display_menu()
      from menu_controllers.main_menu_controller import main_menu_controller
      return main_menu_controller()