from views.tournament_views import TournamentDisplayView, TournamentInputView
from controllers.tournament_controller import TournamentController
from views.player_menu_views import PlayerView
from storage_choice import data_manager
from models.round_utility import update_points
from models.player_utility import get_participating_players_from_data, sort_players_alphabetically
from models.round_models import recreate_rounds


class RoundController:
    """
    Controller class responsible for round management of the application.

    This class handles the creation of new rounds, display of round leaderboards,
    display of alphabetically sorted lists of players, as well as display of round history
    withing a tournament.

    Attributes:
        tournament_controller (TournamentController):
            Logic handler for tournament operations.

        tournament_display_view (TournamentDisplayView):
            View class responsible for display of tournament information.

        tournament_input_view (TournamentInputView):
            View class that handles input related to tournaments.

        player_view (PlayerView):
            View class that handles display and input of player information.

    Methods:
        manage_current_round():
            Handles current round's matches by allowing user to set outcomes.
            Marks round finished and calls on tournament to generate new rounds based on the outcomes.
            Then calls on data_manager to update tournament database.

        show_players_alphabetic():
            Recovers participant data and displays an alphabetically-sorted list of players.

        show_leaderboard():
            Recovers participant data, recreates (player, points) tuples,
            sorts them by number of points and displays participant leaderboard.

        show_round_history():
            Recovers history of all the rounds within a tournament and displays previously generated matches
            contained therein.
    """
    def __init__(
            self,
            tournament_controller=TournamentController,
            tournament_display_view=TournamentDisplayView,
            tournament_input_view=TournamentInputView,
            player_view=PlayerView
            ):
        self.tournament_controller = tournament_controller
        self.display_view = tournament_display_view
        self.input_view = tournament_input_view
        self.player_view = player_view

    def manage_current_round(self, tournament_base_info):
        """Handles current round's matches by allowing user to set outcomes.
           Marks round finished and calls on tournament to generate new rounds based on the outcomes.
           Then calls on data_manager to update tournament database.

           Arguments:
               tournament dictionary
        """

        recreated_tournament = self.tournament_controller.recreate_tournament(tournament_base_info[0])
        current_round = recreated_tournament.get_current_round()
        self.display_view.show_current_round_info(current_round.matches)
        result_list = self.input_view.get_round_results(current_round.matches)
        if result_list is None:
            return None
        if result_list is not None:
            n = 0
            while n < len(result_list):
                update_points(result_list[n],
                              current_round.matches[n],
                              recreated_tournament)
                n += 1
        data_manager.update_player_points_in_db(recreated_tournament)
        recreated_tournament.generate_round()
        data_manager.mark_round_finished(current_round, recreated_tournament)

    def show_players_alphabetic(self, tournament):
        """Recovers participant data and displays an alphabetically-sorted list of players."""

        found_data = data_manager.find_tournament(tournament[0]["name"],
                                                  tournament[0]["dates"])
        participants = get_participating_players_from_data(found_data)
        player_objects = []
        for participant in participants:
            player_objects.append(participant[0])
        sorted_players = sort_players_alphabetically(player_objects)
        self.player_view.display_list_of_players(sorted_players)

    def show_leaderboard(self, tournament):
        """Recovers participant data, recreates (player, points) tuples,
           sorts them by number of points and displays participant leaderboard.

           Arguments:
               tournament dictionary
        """

        found_data = data_manager.find_tournament(tournament[0]["name"],
                                                  tournament[0]["dates"])
        participants = get_participating_players_from_data(found_data)
        players_and_points = []
        for participant in participants:
            player_and_points = tuple()
            player_and_points = (participant[0], participant[2])
            players_and_points.append(player_and_points)
        players_and_points_sorted = sorted(players_and_points,
                                           key=lambda player: player[1],
                                           reverse=True)
        self.display_view.display_leaderboard(players_and_points_sorted)

    def show_round_history(self, tournament):
        """Recovers history of all the rounds within a tournament and displays previously generated matches
           contained therein.

           Arguments:
               tournament dictionary
           """

        found_data = data_manager.find_tournament(tournament[0]["name"],
                                                  tournament[0]["dates"])
        found_rounds = recreate_rounds(found_data["rounds"])
        for round in found_rounds:
            round.recreate_matches()
        for round in found_rounds:
            round.recreate_players()
        self.display_view.display_round_history(found_rounds)
