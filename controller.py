from view import Menu, player_addition_view, display_list_of_players, handle_false_id
from model import Player, list_all_players, check_chess_id_validity
import sys

MAIN_MENU_CHOICES = {"Player management": "1", "Tournament management": "2", "Quit programme": "3"}
PLAYER_MENU_CHOICES = {"Add new player": "1", "Show full list of existing players": "2", "Back to Main Menu": "3"}
TOURNAMENT_MENU_CHOICES = {"Create new tournament": "1", "Manage existing tournament": "2", "Back to Main Menu": "3"}

def handle_add_new_player():
    new_player_data = player_addition_view()
    new_player = Player(new_player_data)
    list_of_all_players = list_all_players()
    all_player_ids = [player.get("chess_national_id") for player in list_of_all_players]
    if check_chess_id_validity(new_player.chess_national_id, all_player_ids) is False:
        while check_chess_id_validity(new_player.chess_national_id, all_player_ids) is False:
            new_player.chess_national_id = handle_false_id()
    new_player.save_player()

def player_menu_controller():
    player_menu = Menu("Player management", PLAYER_MENU_CHOICES)
    decision_player_menu = player_menu.display_menu()
    while decision_player_menu is not PLAYER_MENU_CHOICES["Back to Main Menu"]:
        if decision_player_menu is PLAYER_MENU_CHOICES["Add new player"]:
            handle_add_new_player()
        if decision_player_menu is PLAYER_MENU_CHOICES["Show full list of existing players"]:
            list_of_all_players = list_all_players()
            display_list_of_players(list_of_all_players)
        decision_player_menu = player_menu.display_menu()

def tournament_menu_controller():
    tournament_menu = Menu("Tournament menu", TOURNAMENT_MENU_CHOICES)
    decision_tournament_menu = tournament_menu.display_menu()
    if decision_tournament_menu is TOURNAMENT_MENU_CHOICES["Create new tournament"]:
        pass
    if decision_tournament_menu is TOURNAMENT_MENU_CHOICES["Manage existing tournament"]:
        pass
    if decision_tournament_menu is TOURNAMENT_MENU_CHOICES["Back to Main Menu"]:
        pass
    

def main_menu_controller():
    main_menu = Menu("Main menu", MAIN_MENU_CHOICES)
    decision_main_menu = main_menu.display_menu()
    while decision_main_menu is not MAIN_MENU_CHOICES["Quit programme"]:
        if decision_main_menu is MAIN_MENU_CHOICES["Player management"]:
            player_menu_controller()
        if decision_main_menu is MAIN_MENU_CHOICES["Tournament management"]:
            tournament_menu_controller()
        decision_main_menu = main_menu.display_menu()
    if decision_main_menu is MAIN_MENU_CHOICES["Quit programme"]:
        sys.exit()
    return None

