import re


class TournamentInputView:
    """
    View class responsible for handling tournament-related user inputs.

    This class manages the input and validation of tournament data through the console.
    It uses regular expressions to ensure that user input follows specific formats
    (e.g. names, dates, IDs) and provides feedback when corrections are needed.

    Attributes:
        names_format (Pattern): Validates names (capitalized, optional hyphens/apostrophes).
        numbers_format (Pattern): Validates 2-digit numerical strings.
        date_format (Pattern): Validates dates in 'dd/mm/yyyy' format.
        id_format (Pattern): Validates chess IDs in 'AB00000' format.

    Methods:
        tournament_data_input():
        Collects and returns all required tournament data from user input.
        Returns:
        dict: Dictionary containing tournament name, place, start and end dates,
              description, and number of rounds.

        tournament_name_input():
        Prompts the user to input the tournament name with validation.
        Returns:
        str: Validated tournament name.

        tournament_place_input():
        Prompts the user to input the tournament location with validation.
        Returns:
        str: Validated tournament location.

        tournament_dates_input():
        Prompts the user to input the tournament's start and end dates in dd/mm/yyyy format.
        Returns:
        tuple: (start_date: str, end_date: str) if both are valid.

        tournament_n_of_rounds_input():
        Prompts the user for the number of rounds. Allows optional input,
        defaults to 4 if left blank.
        Returns:
        str: Number of rounds as a string (can be empty).

        tournament_description_input():
        Prompts the user for an optional tournament description with input validation.
        Returns:
        str: Tournament description (can be empty).

        tournament_participants_input(nb_of_participants):
        Collects chess IDs of all participants for a tournament.
        Args:
        nb_of_participants (int): Number of participants to add.
        Returns:
        list: List of participant national chess IDs.

        find_tournament_input():
        Collects tournament name and dates to search for an existing tournament.
        Returns:
        tuple: (tournament_name: str, date_range: str)

        dict_all_data(tournament_data_list):
        Converts a list of tournament values into a dictionary.
        Args:
        tournament_data_list (list): List containing tournament data in fixed order.
        Returns:
        dict: Dictionary of tournament data.

        show_ongoing_tournaments(ongoing_tournaments):
        Displays a list of ongoing tournaments and allows user to select one.
        Args:
        ongoing_tournaments (list): List of dictionaries representing ongoing tournaments.
        Returns:
        str: User's choice as input (tournament key or menu option).

        get_round_results(matches):
        Collects results for a round of matches if the user opts to enter them.
        Args:
        matches (list): List of tuples containing match player objects.
        Returns:
        list | None: List of match results (winner ID or 'draw'), or None if skipped.
    """
    def __init__(self):
        self.names_format = re.compile(r'^[a-zA-Z0-9,. ]*$')
        self.numbers_format = re.compile(r"^[0-9]{2}$")
        self.date_format = re.compile(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$")
        self.id_format = re.compile(r"[A-Z]{2}[0-9]{5}$")

    def tournament_data_input(self):
        """
        Collects and returns all required tournament data from user input.

        Returns:
        dict: Dictionary containing tournament name, place, start and end dates,
              description, and number of rounds.
        """
        tournament_data_list = []
        tournament_data_list.append(self.tournament_name_input())
        tournament_data_list.append(self.tournament_place_input())
        beginning_and_end = self.tournament_dates_input()
        tournament_data_list.append(beginning_and_end[0])
        tournament_data_list.append(beginning_and_end[1])
        tournament_data_list.append(self.tournament_description_input())
        tournament_data_list.append(self.tournament_n_of_rounds_input())
        all_data_dict = self.dict_all_data(tournament_data_list)
        return all_data_dict

    def tournament_name_input(self):
        """
        Prompts the user to input the tournament name with validation.

        Returns:
        str: Validated tournament name.
        """
        print("Please enter new tournament information")
        tournmnt_name = input("Please enter the name of the tournament: ")
        while not self.names_format.fullmatch(tournmnt_name):
            print("Please avoid any characters other than letters, "
                  "numbers, dots and commas")
            tournmnt_name = input("Please enter the name of the tournament: ")
        return tournmnt_name

    def tournament_place_input(self):
        """
        Prompts the user to input the tournament location with validation.

        Returns:
        str: Validated tournament location.
        """
        tournament_place = input("Please enter where this "
                                 "tournament will take place: ")
        while not self.names_format.fullmatch(tournament_place):
            print(("Please avoid any characters other than letters, "
                   "numbers, dots and commas"))
            tournament_place = input("Please enter where this "
                                     "tournament will take place: ")
        return tournament_place

    def tournament_dates_input(self):
        """
        Prompts the user to input the tournament's start and end dates in dd/mm/yyyy format.

        Returns:
        tuple: (start_date: str, end_date: str) if both are valid.
        """
        tournament_beginning_date = input("Please enter "
                                          "the start date "
                                          "of the tournament "
                                          "in dd/mm/yyyy format: ")
        while not self.date_format.fullmatch(tournament_beginning_date):
            print("Please use the dd/mm/yyyy format")
            tournament_beginning_date = input("Please enter "
                                              "the start date "
                                              "of the tournament "
                                              "in dd/mm/yyyy format: ")
        tournament_end_date = input("Please enter "
                                    "the end date of this tournament "
                                    "in dd/mm/yyyy format: ")
        while not self.date_format.fullmatch(tournament_end_date):
            print("Please use the dd/mm/yyyy format")
            tournament_end_date = input("Please enter "
                                        "the end date of this tournament "
                                        "in dd/mm/yyyy format: ")
        return tournament_beginning_date, tournament_end_date

    def tournament_n_of_rounds_input(self):
        """
        Prompts the user for the number of rounds. Allows optional input,
        defaults to 4 if left blank.

        Returns:
        str: Number of rounds as a string (can be empty).
        """
        tournament_number_of_rounds = input("Please enter "
                                            "the number of rounds "
                                            "to take place "
                                            "(optional, defaults to 4): ")
        num = tournament_number_of_rounds
        while num != "" and not self.numbers_format.fullmatch(num):
            print("Please enter a valid number of rounds, use only numbers, "
                  "up to two digits or just press enter")
            tournament_number_of_rounds = input("Please enter "
                                                "the number of rounds "
                                                "to take place "
                                                "(optional, defaults to 4): ")
            num = tournament_number_of_rounds
        return tournament_number_of_rounds

    def tournament_description_input(self):
        """
        Prompts the user for an optional tournament description with input validation.

        Returns:
        str: Tournament description (can be empty).
        """
        tournament_description = input("Please enter "
                                       "a description for this tournament "
                                       "(optional): ")
        desc = tournament_description
        while desc != "" and not self.names_format.fullmatch(desc):
            print("Please avoid using characters other than letters, numbers, "
                  "commas and dots or leaving it empty")
            tournament_description = input("Please enter "
                                           "a description for this tournament "
                                           "(optional): ")
            desc = tournament_description
        return tournament_description

    def tournament_participants_input(self, nb_of_participants):
        """
        Collects chess IDs of all participants for a tournament.

        Args:
        nb_of_participants (int): Number of participants to add.

        Returns:
        list: List of participant national chess IDs.
        """
        counter = 0
        players = []
        print(
            "Add players to the new tournament. "
            "Enter player's national chess id in the following format: "
            "ID00000"
         )
        while counter != nb_of_participants:
            new_player = input(f"Add player number {counter+1}: ")
            while not self.id_format.fullmatch(new_player):
                print("Please enter this participant's id in the following format: "
                      "ID00000")
                new_player = input(f"Add player number {counter+1}: ")
            players.append(new_player)
            counter = counter + 1
        return players

    def find_tournament_input(self):
        """
        Collects tournament name and dates to search for an existing tournament.

        Returns:
        tuple: (tournament_name: str, date_range: str)
        """
        print("Tournament search")
        name = input("Please insert tournament name: ")
        while not self.names_format.fullmatch(name):
            print("Please avoid using anything but letters, numbers, "
                  "commas, spaces and dots")
            name = input("Please insert tournament name: ")
        date_beginning = input("Please insert tournament start date "
                               "in a 'dd/mm/yyyy' format: ")
        while not self.date_format.fullmatch(date_beginning):
            print("Please use the 'dd/mm/yyyy' format, "
                  "note that days and months must be two digits. "
                  "Ex: 06/06/2025")
            date_beginning = input("Please insert tournament start date "
                                   "in a 'dd/mm/yyyy' format: ")
        date_end = input("Please insert tournament end date "
                         "in a 'dd/mm/yyyy' format: ")
        while not self.date_format.fullmatch(date_end):
            print("Please use the 'dd/mm/yyyy' format, "
                  "note that days and months must be two digits. "
                  "Ex: 06/06/2025")
            date_end = input("Please insert tournament end date "
                             "in a 'dd/mm/yyyy' format: ")
        dates = f"{date_beginning} - {date_end}"
        return name, dates

    @staticmethod
    def dict_all_data(tournament_data_list):
        """
        Converts a list of tournament values into a dictionary.

        Args:
        tournament_data_list (list): List containing tournament data in fixed order.

        Returns:
        dict: Dictionary of tournament data.
        """
        return {
            "tournament_name":
            tournament_data_list[0],
            "tournament_place":
            tournament_data_list[1],
            "tournament_beginning_date":
            tournament_data_list[2],
            "tournament_end_date":
            tournament_data_list[3],
            "tournament_description":
            tournament_data_list[4],
            "number_of_rounds":
            tournament_data_list[5]
        }

    @staticmethod
    def show_ongoing_tournaments(ongoing_tournaments):
        """
        Displays a list of ongoing tournaments and allows user to select one.

        Args:
        ongoing_tournaments (list): List of dictionaries representing ongoing tournaments.

        Returns:
        str: User's choice as input (tournament key or menu option).
        """
        if (ongoing_tournaments) == []:
            print("No ongoing tournaments")
            return None
        print("Choose ongoing tournament: ")
        for tournament in ongoing_tournaments:
            print(f"{tournament['key']}: "
                  f"{tournament['name']}, {tournament['dates']}")
        print(f"{ongoing_tournaments[-1]['key'] + 1}: Back to Tournament Menu")
        choice = input(">>> ")
        while int(choice) > ongoing_tournaments[-1]["key"] + 1:
            print("Please enter a valid option: ")
            choice = input(">>> ")
        return choice

    @staticmethod
    def get_round_results(matches):
        """
        Collects results for a round of matches if the user opts to enter them.

        Args:
        matches (list): List of tuples containing match player objects.

        Returns:
        list | None: List of match results (winner ID or 'draw'), or None if skipped.
        """
        print("Would you like to add results to these matches? Y/N")
        choice = input(">>> ")
        if choice == "Y":
            matches_result_list = []
            for match in matches:
                print((f"{match[0].player.surname} "
                       f"{match[0].player.name} "
                       f"{match[0].player.chess_national_id} "
                       "vs "
                       f"{match[1].player.surname} "
                       f"{match[1].player.name} "
                       f"{match[1].player.chess_national_id}"))
                print("Please enter winner's id or type 'draw'")
                result = input(">>> ")
                player1_id = f"{match[0].player.chess_national_id}"
                player2_id = f"{match[1].player.chess_national_id}"
                while result not in ("draw", player1_id, player2_id):
                    print("Please enter a valid player's id or type 'draw'")
                    result = input(">>> ")
                matches_result_list.append(result)
            return matches_result_list
        else:
            return None


class TournamentDisplayView:
    """
    View class for display of tournament-related information.

    Attributes:
    None

    Methods:
    display_all_tournaments(all_tournaments):
    Prints out information of all tournaments given in argument.
    Args:
    List of Tournament objects

    display_round_history(rounds):
    Prints round information containing name of each round and the matches contained therein.
    Args:
    List of FirstRound and SubsequentRound objects containing TournamentPlayer objects.

    tournament_not_found():
    Prints out 'Tournament not found'

    display_leaderboard(players_and_points):
    Prints out a list of players sorted by the number of points in form of a leaderboard.
    Args:
    Sorted list of tuples containing (Player, number of points (int))

    show_current_round_info(matches):
    Prints out list of matches in the currently ongoing round.
    Args:
    List of match tuples (TournamentPlayer, TournamentPlayer)
    """
    def display_all_tournaments(self, all_tournaments):
        """
        Prints out information of all tournaments given in argument.

        Args:
        List of Tournament objects
        """
        print("")
        for tournament in all_tournaments:
            print(f"Name: {tournament.name}")
            print(f"Place: {tournament.place}")
            print(f"Dates: {tournament.dates}")
            print(f"Description: {tournament.description}\n")
            print(f"Current round: {tournament.current_round}\n")
            print("Players: ")
            for player in tournament.players_list:
                print(f"{player.player.surname} {player.player.name}, "
                      f"{player.player.chess_national_id}")
            print("\nRounds: ")
            self.display_round_history(tournament.rounds)
            print("")

    @staticmethod
    def display_round_history(rounds):
        """
        Prints round information containing name of each round and the matches contained therein.

        Args:
        List of FirstRound and SubsequentRound objects containing TournamentPlayer objects.
        """
        for round in rounds:
            print(round.name)
            for match in round.matches:
                print(f"{match[0].player.surname} {match[0].player.name}, "
                      f"{match[0].player.chess_national_id} "
                      f"pts: {match[0].tournament_points} "
                      "vs "
                      f"{match[1].player.surname} {match[1].player.name}, "
                      f"{match[1].player.chess_national_id} "
                      f"pts: {match[1].tournament_points}")

    @staticmethod
    def tournament_not_found():
        """Prints out 'Tournament not found'"""
        print("\nTournament not found!\n")

    @staticmethod
    def display_leaderboard(players_and_points):
        """
        Prints out a list of players sorted by the number of points in form of a leaderboard.

        Args:
        Sorted list of tuples containing (Player, number of points (int))
        """
        for player in players_and_points:
            print(f"pts: {player[1]}. "
                  f"{player[0].surname} {player[0].name}, "
                  f"{player[0].chess_national_id}")

    @staticmethod
    def show_current_round_info(matches):
        """
        Prints out list of matches in the currently ongoing round.
        Args:
        List of match tuples (TournamentPlayer, TournamentPlayer)
        """
        for match in matches:
            print((f"{match[0].player.surname} "
                   f"{match[0].player.name} "
                   f"{match[0].player.chess_national_id} "
                   "vs "
                   f"{match[1].player.surname} "
                   f"{match[1].player.name} "
                   f"{match[1].player.chess_national_id}"))
