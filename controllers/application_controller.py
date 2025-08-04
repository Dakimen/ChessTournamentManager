from controllers.menu_controllers import MenuController
from views.tournament_views import TournamentInputView, TournamentDisplayView
from views.player_menu_views import PlayerView
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.round_controller import RoundController


class AppContext:
    """
    Initializes and holds references to all major components of the application.

    This class sets up the views, controllers, and injects dependencies needed by
    the MenuController to run the application in a decoupled and modular way.

    Attributes:
        tournament_input (TournamentInputView): Handles input related to tournaments.
        tournament_display (TournamentDisplayView): Handles display of tournament information.
        player_view (PlayerView): Handles player input and output.
        player_controller (PlayerController): Logic handler for player operations.
        tournament_controller (TournamentController): Logic handler for tournament operations.
        round_controller (RoundController): Manages current round, leaderboard, and history.
        menu_controller (MenuController): Manages user interaction with menus.
    """
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
    """
    Entry point for the application.

    This class is responsible for initializing the application context and
    launching the main menu interface.

    Attributes:
        context (AppContext): Application context holding all controllers and views.

    Methods:
        run(): Starts the main menu loop of the application.
    """
    def __init__(self):
        self.context = AppContext()

    def run(self):
        """Starts the main menu loop of the application.
           Takes no arguments."""
        self.context.menu_controller.display_main_menu()
        return None
