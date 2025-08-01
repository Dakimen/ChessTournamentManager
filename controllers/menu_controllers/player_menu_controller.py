from controllers.player_controllers import player_controller
from views.menu import Menu

PLAYER_MENU_CHOICES = {
    "1": {"text": "Add new player",
          "key": "1",
          "action": player_controller.handle_add_new_player},
    "2": {"text": "Show full list of existing players",
          "key": "2",
          "action": player_controller.get_all_players_alphabetically},
    "3": {"text": "Back to Main Menu",
          "key": "3",
          "action": None}
    }


def player_menu_controller():
    player_menu = Menu("Player management", PLAYER_MENU_CHOICES)
    decision = player_menu.display_menu()
    if PLAYER_MENU_CHOICES[decision]["text"] != "Back to Main Menu":
        while PLAYER_MENU_CHOICES[decision]["text"] != "Back to Main Menu":
            PLAYER_MENU_CHOICES[decision]["action"]()
            decision = player_menu.display_menu()
    from controllers.menu_controllers.main_menu_controller import (
        main_menu_controller
        )
    return main_menu_controller()
