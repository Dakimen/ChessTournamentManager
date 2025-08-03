from controllers.menu_controllers import MenuController
from views.tournament_views import TournamentInputView, TournamentDisplayView
from views.player_menu_views import PlayerView
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.round_controller import RoundController


class AppContext:
    def __init__(self):
        self.tournament_input = TournamentInputView()
        self.tournament_display = TournamentDisplayView()
        self.player_view = PlayerView()
        self.player_controller = PlayerController(self.player_view)
        self.tournament_controller = TournamentController(
            self.tournament_display,
            self.tournament_input,
            self.player_view
        )
        self.round_controller = RoundController(
            self.tournament_controller,
            self.tournament_display,
            self.tournament_input,
            self.player_view
            )
        self.menu_controller = MenuController(
            self.tournament_input,
            self.tournament_display,
            self.tournament_controller,
            self.player_controller,
            self.round_controller
            )


class ApplicationController:
    def __init__(self):
        self.context = AppContext()

    def run(self):
        self.context.menu_controller.display_main_menu()
        return None
