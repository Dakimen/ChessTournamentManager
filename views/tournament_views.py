import re

def tournament_data_input():
    suitable_names = re.compile(r'^[a-zA-Z0-9,. ]*$')
    suitable_numbers = re.compile(r"^[0-9]{2}$")
    suitable_dates = re.compile(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}")
    tournament_data_list = []
    tournament_data_list.append(tournament_name_input(suitable_names))
    tournament_data_list.append(tournament_place_input(suitable_names))
    beginning_and_end = tournament_dates_input(suitable_dates)
    tournament_data_list.append(beginning_and_end[0])
    tournament_data_list.append(beginning_and_end[1])
    tournament_data_list.append(tournament_n_of_rounds_input(suitable_numbers))
    tournament_data_list.append(tournament_description_input(suitable_names))
    all_data_dict = dict_all_data(tournament_data_list)
    return all_data_dict

def tournament_name_input(suitable_names):
    print("Please enter new tournament information")
    tournament_name = input("Please enter the name of the new tournament: ")
    while not suitable_names.fullmatch(tournament_name):
        print("Please avoid any characters other than letters, numbers, dots and commas")
        tournament_name = input("Please enter the name of the new tournament: ")
    return tournament_name

def tournament_place_input(suitable_names):
    tournament_place = input("Please enter where this tournament will take place: ")
    while not suitable_names.fullmatch(tournament_place):
        print("Please avoid any characters other than letters, numbers, dots and commas")
        tournament_place = input("Please enter where this tournament will take place: ")
    return tournament_place

def tournament_dates_input(suitable_dates):
    tournament_beginning_date = input("Please enter the start date of the tournament in dd/mm/yyyy format: ")
    while not suitable_dates.fullmatch(tournament_beginning_date):
        print("Please use the dd/mm/yyyy format")
        tournament_beginning_date = input("Please enter the start date of the tournament in dd/mm/yyyy format: ")
    tournament_end_date = input("Please enter the end date of this tournament in dd/mm/yyyy format: ")
    while not suitable_dates.fullmatch(tournament_end_date):
        print("Please use the dd/mm/yyyy format")
        tournament_end_date = input("Please enter the end date of this tournament in dd/mm/yyyy format: ")
    return tournament_beginning_date, tournament_end_date

def tournament_n_of_rounds_input(suitable_numbers):
    tournament_number_of_rounds = input("Please enter the number of rounds to take place (optional, defaults to 4): ")
    while tournament_number_of_rounds != "" and not suitable_numbers.fullmatch(tournament_number_of_rounds):
        print("Please enter a valid number of rounds, use only numbers, up to two digits or just press enter")
        tournament_number_of_rounds = input("Please enter the number of rounds to take place (optional, defaults to 4): ")
    return tournament_number_of_rounds

def tournament_description_input(suitable_characters):
    tournament_description = input("Please enter a description for this tournament (optional): ")
    while tournament_description != "" and not suitable_characters.fullmatch(tournament_description):
        print("Please avoid using characters other than letters, numbers, commas and dots or leaving it empty")
        tournament_description = input("Please enter a description for this tournament (optional): ")
    return tournament_description

def dict_all_data(tournament_data_list):
    all_data = {
                "tournament_name": f"{tournament_data_list[0]}", 
                "tournament_place": f"{tournament_data_list[1]}",
                "tournament_beginning_date": f"{tournament_data_list[2]}",
                "tournament_end_date": f"{tournament_data_list[3]}",
                "tournament_description": f"{tournament_data_list[4]}",
                "number_of_rounds": f"{tournament_data_list[5]}"
                }
    return all_data

def tournament_participants_input(nb_of_participants):
    acceptable_format = re.compile(r"^[A-Z][a-z]*(?:[-'][A-Z][a-z]*)*, [A-Z][a-z]*(?:[-'][A-Z][a-z]*)*, [A-Z]{2}[0-9]{5}$")
    counter = 0
    players = []
    print(
          "Add players to the new tournament. Players must be written in the following format: "
          "surname, name, national_chess_id"
         )
    while counter != nb_of_participants:
        new_player = input(f"Add player number {counter+1}: ")
        if not acceptable_format.fullmatch(new_player):
            while not acceptable_format.fullmatch(new_player):
                print("Please enter this participant's info in a valid 'Surname, Name, ID00000' format")
                new_player = input(f"Add player number {counter+1}: ")
        players.append(new_player)
        counter = counter + 1
    return players

def show_ongoing_tournaments(ongoing_tournaments):
    if(ongoing_tournaments) == []:
        print("No ongoing tournaments")
        return None
    print("Choose ongoing tournament: ")
    for tournament in ongoing_tournaments:
        print(f"{tournament["key"]}: {tournament["name"]}, {tournament["dates"]}")
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

