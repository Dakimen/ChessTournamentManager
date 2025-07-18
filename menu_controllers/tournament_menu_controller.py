from view import Menu, tournament_data_input
from model import Tournament

TOURNAMENT_MENU_CHOICES = {"Create new tournament": "1", "Manage existing tournament": "2", "Back to Main Menu": "3"}

def tournament_menu_controller():
    tournament_menu = Menu("Tournament menu", TOURNAMENT_MENU_CHOICES)
    decision_tournament_menu = tournament_menu.display_menu()
    if decision_tournament_menu is TOURNAMENT_MENU_CHOICES["Create new tournament"]:
        tournament_data = tournament_data_input()
        new_tournament = Tournament(tournament_data)
        new_tournament.save_tournament()
    if decision_tournament_menu is TOURNAMENT_MENU_CHOICES["Manage existing tournament"]:
        pass
    if decision_tournament_menu is TOURNAMENT_MENU_CHOICES["Back to Main Menu"]:
        pass
    