from models.player_models import Player
from models.tournament_models import Tournament
from views.tournament_views import TournamentDisplayView, TournamentInputView
from views.player_menu_views import PlayerView
from models.tournament_utility import recreate_tournament_input
from models.round_models import recreate_rounds
from models.player_utility import get_participating_players_from_data
from storage_choice import data_manager


class TournamentController:
    def __init__(
            self,
            tourn_display=TournamentDisplayView,
            tourn_input=TournamentInputView,
            player_view=PlayerView
            ):
        self.tour_display = tourn_display
        self.tour_input = tourn_input
        self.player_view = player_view

    def manage_create_tournament(self):
        tournament_data = self.tour_input.tournament_data_input()
        n_of_rounds = tournament_data["number_of_rounds"]
        nb_players = self.calculate_number_of_players(n_of_rounds)
        players_raw_input = self.tour_input.tournament_participants_input(nb_players)
        players = self.get_tournament_players(players_raw_input)
        new_tournament = Tournament(tournament_data, players)
        new_tournament.generate_round()
        new_tournament.save_tournament()

    def handle_not_in_db(self, new_player_id):
        new_player = self.player_view.get_data(new_player_id)
        unreg_player = Player(new_player)
        unreg_player.save_player()
        return unreg_player

    def get_tournament_players(self, players_raw_input):
        tournament_players = []
        for player_id in players_raw_input:
            new_player = {"chess_national_id": player_id}
            if data_manager.check_if_in_db(new_player) is False:
                unreg_player = self.handle_not_in_db(new_player)
                tournament_players.append(unreg_player)
            else:
                reg_player_data = data_manager.get_player_from_db(new_player)
                reg_player = Player(reg_player_data)
                tournament_players.append(reg_player)
        return tournament_players

    def recreate_tournament(self, tournament_base_info):
        found_data = data_manager.find_tournament(tournament_base_info["name"],
                                                  tournament_base_info["dates"])
        if found_data is None:
            self.tour_display.tournament_not_found()
            return None
        tourn_input = recreate_tournament_input(found_data)
        participants = get_participating_players_from_data(found_data)
        found_rounds = recreate_rounds(found_data["rounds"])
        for round in found_rounds:
            round.recreate_matches()
        for round in found_rounds:
            round.recreate_players()
        current_round = int(found_data["current_round"])
        recreated_tournament = Tournament(tourn_input, participants, found_rounds, current_round)
        return recreated_tournament

    def list_all_tournaments(self):
        tournaments = data_manager.get_all_tournaments()
        recreated_tournaments = []
        for tournament in tournaments:
            recreated_tournament = self.recreate_tournament(tournament)
            if recreated_tournament is None:
                return None
            recreated_tournaments.append(recreated_tournament)
        self.tour_display.display_all_tournaments(recreated_tournaments)

    def find_a_tournament(self):
        name_and_dates = self.tour_input.find_tournament_input()
        tournament_data = {"name": name_and_dates[0], "dates": name_and_dates[1]}
        recreated_tournament = self.recreate_tournament(tournament_data)
        if recreated_tournament is None:
            return None
        tournaments = []
        tournaments.append(recreated_tournament)
        self.tour_display.display_all_tournaments(tournaments)

    @staticmethod
    def calculate_number_of_players(nb_rounds):
        if nb_rounds == "":
            nb_rounds = 4
        else:
            nb_rounds = int(nb_rounds)
        nb_players = nb_rounds + 1
        return nb_players
