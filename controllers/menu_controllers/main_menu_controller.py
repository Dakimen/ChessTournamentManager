from views.menu import Menu
import sys
from controllers.menu_controllers.player_menu_controller import (
    player_menu_controller
    )
from controllers.menu_controllers.tournament_menu_controller import (
    tournament_menu_controller
    )

MAIN_MENU_CHOICES = {
    "1": {"text": "Player management",
          "key": "1", "action": player_menu_controller},
    "2": {"text": "Tournament management",
          "key": "2", "action": tournament_menu_controller},
    "3": {"text": "Quit programme",
          "key": "3", "action": sys.exit}
}


def main_menu_controller():
    main_menu = Menu("Main menu", MAIN_MENU_CHOICES)
    decision_main_menu = main_menu.display_menu()
    return MAIN_MENU_CHOICES[decision_main_menu]["action"]()
