from views.main_view import tournament_data_input
from models.model import Tournament

def manage_create_tournament():
    tournament_data = tournament_data_input()
    new_tournament = Tournament(tournament_data)
    new_tournament.save_tournament()