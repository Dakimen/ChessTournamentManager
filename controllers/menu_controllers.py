from views.menu import Menu
from views.tournament_views import TournamentDisplayView, TournamentInputView
from controllers.tournament_controller import TournamentController
from controllers.player_controller import PlayerController
from controllers.round_controller import RoundController
from storage_choice import data_manager

class MenuController:
    def __init__(
            self,
            tournament_input=TournamentInputView,
            tournament_display=TournamentDisplayView,
            tournament_controller=TournamentController,
            player_controller=PlayerController,
            round_controller=RoundController
            ):
        self.tournament_input = tournament_input
        self.tournament_display = tournament_display
        self.tournament_controller = tournament_controller
        self.player_controller = player_controller
        self.round_controller = round_controller
        self.main_menu_options = {
        "1": {"text": "Player management",
              "key": "1",
              "action": self.display_player_menu},
        "2": {"text": "Tournament management",
              "key": "2",
              "action": self.display_tournament_menu},
        "Q": {"text": "Quit programme",
              "key": "Q",
              "action": None}
        }

        self.player_menu_options = {
            "1": {"text": "Add new player",
                  "key": "1",
                  "action": self.player_controller.handle_add_new_player},
            "2": {"text": "Show full list of existing players",
                  "key": "2",
                  "action": self.player_controller.get_all_players_alphabetically},
            "Q": {"text": "Back to Main Menu",
                  "key": "3",
                  "action": None}
        }

        self.tournament_menu_options = {
            "1": {"text": "Create new tournament",
                  "key": "1", "action": self.tournament_controller.manage_create_tournament},
            "2": {"text": "Manage ongoing tournaments",
                  "key": "2", "action": self.ongoing_tournaments_list_menu},
            "3": {"text": "List all tournaments",
                  "key": "3", "action": self.tournament_controller.list_all_tournaments},
            "4": {"text": "Find a tournament",
                  "key": "4", "action": self.tournament_controller.find_a_tournament},
            "5": {"text": "Back to Main Menu",
                  "key": "5", "action": None}
        }

        self.unfinished_tournament_options = {
            "1": {"text": "Manage current round",
                  "key": "1", "action": self.round_controller.manage_current_round},
            "2": {"text": "Show leaderboard",
                  "key": "2", "action": self.round_controller.show_leaderboard},
            "3": {"text": "List all players alphabetically",
                  "key": "3", "action": self.round_controller.show_players_alphabetic},
            "4": {"text": "Show round history",
                  "key": "4", "action": self.round_controller.show_round_history},
            "5": {"text": "Back to previous menu",
                  "key": "5", "action": None}
        }

    def display_main_menu(self):
        main_menu = Menu("Main menu", self.main_menu_options)
        decision_main_menu = main_menu.display_menu()
        action = self.main_menu_options[decision_main_menu]["action"]
        if action:
            action()
        while decision_main_menu != "Q" and decision_main_menu != "q":
            decision_main_menu = main_menu.display_menu()
            action = self.main_menu_options[decision_main_menu]["action"]
            if action:
                action()
        return None

    def display_player_menu(self):
        player_menu = Menu("Player management", self.player_menu_options)
        decision = player_menu.display_menu()
        while self.player_menu_options[decision]["text"] != "Back to Main Menu":
            action = self.player_menu_options[decision]["action"]()
            if action:
                action()
            decision = player_menu.display_menu()
        return None

    def display_tournament_menu(self):
        tournament_menu = Menu("Tournament menu", self.tournament_menu_options)
        decision = tournament_menu.display_menu()
        decision_text = self.tournament_menu_options[decision]["text"]
        if decision_text != "Back to Main Menu":
            while decision_text != "Back to Main Menu":
                self.tournament_menu_options[decision]["action"]()
                decision = tournament_menu.display_menu()
                decision_text = self.tournament_menu_options[decision]["text"]
        else:
            return None

    def ongoing_tournament_menu(self, chosen_tournament):
        tourn_management_menu = Menu(f"{chosen_tournament[0]["name"]} menu",
                                     self.unfinished_tournament_options)
        choice = tourn_management_menu.display_menu()
        choice_text = self.unfinished_tournament_options[choice]["text"]
        if choice_text != "Back to previous menu":
            while choice_text != "Back to previous menu":
                self.unfinished_tournament_options[choice]["action"](chosen_tournament)
                choice = tourn_management_menu.display_menu()
                choice_text = self.unfinished_tournament_options[choice]["text"]
        else:
            return None
 
    def ongoing_tournaments_list_menu(self):
        all_tournaments = data_manager.get_all_tournaments()
        ongoing_tournaments = []
        for tournament in all_tournaments:
            unfinished_rounds = []
            for round in tournament["rounds"]:
                if round["finished"] is False:
                    unfinished_rounds.append(round)
            if unfinished_rounds != []:
                ongoing_tournaments.append(tournament)
        ongoing_tournaments_info = []
        key = 1
        for tournament in ongoing_tournaments:
            ongoing_dict = {"name": tournament["name"],
                            "dates": tournament["dates"], "key": key}
            ongoing_tournaments_info.append(ongoing_dict)
            key += 1
        choice = self.tournament_input.show_ongoing_tournaments(ongoing_tournaments_info)
        if choice is None:
            return None
        if int(choice) == ongoing_tournaments_info[-1]["key"] + 1:
            return None
        chosen_tournament = []
        for tournament in ongoing_tournaments_info:
            if tournament["key"] == int(choice):
                chosen_tournament.append(tournament)
        return self.ongoing_tournament_menu(chosen_tournament)
