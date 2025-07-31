import re
from views.round_views import display_round_history


def tournament_data_input():
    names_format = re.compile(r'^[a-zA-Z0-9,. ]*$')
    numbers_formt = re.compile(r"^[0-9]{2}$")
    dates_formt = re.compile(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$")
    tournament_data_list = []
    tournament_data_list.append(tournament_name_input(names_format))
    tournament_data_list.append(tournament_place_input(names_format))
    beginning_and_end = tournament_dates_input(dates_formt)
    tournament_data_list.append(beginning_and_end[0])
    tournament_data_list.append(beginning_and_end[1])
    tournament_data_list.append(tournament_description_input(names_format))
    tournament_data_list.append(tournament_n_of_rounds_input(numbers_formt))
    all_data_dict = dict_all_data(tournament_data_list)
    return all_data_dict


def tournament_name_input(suitable_names):
    print("Please enter new tournament information")
    tournmnt_name = input("Please enter the name of the tournament: ")
    while not suitable_names.fullmatch(tournmnt_name):
        print("Please avoid any characters other than letters, "
              "numbers, dots and commas")
        tournmnt_name = input("Please enter the name of the tournament: ")
    return tournmnt_name


def tournament_place_input(suitable_names):
    tournament_place = input("Please enter where this "
                             "tournament will take place: ")
    while not suitable_names.fullmatch(tournament_place):
        print(("Please avoid any characters other than letters, "
               "numbers, dots and commas"))
        tournament_place = input("Please enter where this "
                                 "tournament will take place: ")
    return tournament_place


def tournament_dates_input(suitable_dates):
    tournament_beginning_date = input("Please enter "
                                      "the start date "
                                      "of the tournament "
                                      "in dd/mm/yyyy format: ")
    while not suitable_dates.fullmatch(tournament_beginning_date):
        print("Please use the dd/mm/yyyy format")
        tournament_beginning_date = input("Please enter "
                                          "the start date "
                                          "of the tournament "
                                          "in dd/mm/yyyy format: ")
    tournament_end_date = input("Please enter "
                                "the end date of this tournament "
                                "in dd/mm/yyyy format: ")
    while not suitable_dates.fullmatch(tournament_end_date):
        print("Please use the dd/mm/yyyy format")
        tournament_end_date = input("Please enter "
                                    "the end date of this tournament "
                                    "in dd/mm/yyyy format: ")
    return tournament_beginning_date, tournament_end_date


def tournament_n_of_rounds_input(suitable_numbers):
    tournament_number_of_rounds = input("Please enter "
                                        "the number of rounds "
                                        "to take place "
                                        "(optional, defaults to 4): ")
    num = tournament_number_of_rounds
    while num != "" and not suitable_numbers.fullmatch(num):
        print("Please enter a valid number of rounds, use only numbers, "
              "up to two digits or just press enter")
        tournament_number_of_rounds = input("Please enter "
                                            "the number of rounds "
                                            "to take place "
                                            "(optional, defaults to 4): ")
        num = tournament_number_of_rounds
    return tournament_number_of_rounds


def tournament_description_input(suitable_characters):
    tournament_description = input("Please enter "
                                   "a description for this tournament "
                                   "(optional): ")
    desc = tournament_description
    while desc != "" and not suitable_characters.fullmatch(desc):
        print("Please avoid using characters other than letters, numbers, "
              "commas and dots or leaving it empty")
        tournament_description = input("Please enter "
                                       "a description for this tournament "
                                       "(optional): ")
        desc = tournament_description
    return tournament_description


def dict_all_data(tournament_data_list):
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


def tournament_participants_input(nb_of_participants):
    acceptable_format = re.compile(r"^[A-Z][a-z]*(?:[-'][A-Z][a-z]*)*, "
                                   r"[A-Z][a-z]*(?:[-'][A-Z][a-z]*)*, "
                                   r"[A-Z]{2}[0-9]{5}$")
    counter = 0
    players = []
    print(
          "Add players to the new tournament. "
          "Players must be written in the following format: "
          "surname, name, national_chess_id"
         )
    while counter != nb_of_participants:
        new_player = input(f"Add player number {counter+1}: ")
        if not acceptable_format.fullmatch(new_player):
            while not acceptable_format.fullmatch(new_player):
                print("Please enter this participant's info in a valid "
                      "'Surname, Name, ID00000' format")
                new_player = input(f"Add player number {counter+1}: ")
        players.append(new_player)
        counter = counter + 1
    return players


def show_ongoing_tournaments(ongoing_tournaments):
    if (ongoing_tournaments) == []:
        print("No ongoing tournaments")
        return None
    print("Choose ongoing tournament: ")
    for tournament in ongoing_tournaments:
        print(f"{tournament["key"]}: "
              f"{tournament["name"]}, {tournament["dates"]}")
    print(f"{ongoing_tournaments[-1]["key"] + 1}: Back to Tournament Menu")
    choice = input(">>> ")
    while int(choice) > ongoing_tournaments[-1]["key"] + 1:
        print("Please enter a valid option: ")
        choice = input(">>> ")
    return choice


def show_current_round_info(matches):
    for match in matches:
        print((f"{match[0].player.surname} "
               f"{match[0].player.name} "
               f"{match[0].player.chess_national_id} "
               "vs "
               f"{match[1].player.surname} "
               f"{match[1].player.name} "
               f"{match[1].player.chess_national_id}"))


def get_round_results(matches):
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
            matches_result_list.append(result)
        return matches_result_list
    else:
        return None


def display_leaderboard(players_and_points):
    for player in players_and_points:
        print(f"pts: {player[1]}. "
              f"{player[0].surname} {player[0].name}, "
              f"{player[0].chess_national_id}")


def display_all_tournaments(all_tournaments):
    print("")
    for tournament in all_tournaments:
        print(f"Name: {tournament.name}")
        print(f"Place: {tournament.place}")
        print(f"Dates: {tournament.dates}")
        print(f"Description: {tournament.description}")
        print("Players: ")
        for player in tournament.players_list:
            print(f"{player.player.surname} {player.player.name}, "
                  f"{player.player.chess_national_id}")
        print("Rounds: ")
        display_round_history(tournament.rounds)
        print("")


def find_tournament_input():
    suitable_names = re.compile(r'^[a-zA-Z0-9,. ]*$')
    suitable_dates = re.compile(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}"
                                r" - "
                                r"[0-9]{2}/[0-9]{2}/[0-9]{4}$")
    print("Tournament search")
    name = input("Please insert tournament name: ")
    while not suitable_names.fullmatch(name):
        print("Please avoid using anything but letters, numbers, "
              "commas, spaces and dots")
        name = input("Please insert tournament name: ")
    dates = input("Please insert tournament dates "
                  "in a 'dd/mm/yyyy - dd/mm/yyyy' format: ")
    while not suitable_dates.fullmatch(dates):
        print("Please use the 'dd/mm/yyyy - dd/mm/yyyy' format, "
              "note that days and months must be two digits. "
              "Ex: 06/06/2025 - 07/07/2025")
        dates = input("Please insert tournament dates "
                      "in a 'dd/mm/yyyy - dd/mm/yyyy' format: ")
    return name, dates


def tournament_not_found():
    print("\nTournament not found!\n")
