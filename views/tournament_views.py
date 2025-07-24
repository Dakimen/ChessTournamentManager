def tournament_data_input():
    print("Please enter new tournament information")
    tournament_name = input("Please enter the name of the new tournament: ")
    tournament_place = input("Please enter where this tournament will take place: ")
    tournament_beginning_date = input("Please enter the start date of the tournament: ")
    tournament_end_date = input("Please enter the end date of this tournament: ")
    tournament_number_of_rounds = input("Please enter the number of rounds to take place (optional, defaults to 4): ")
    tournament_description = input("Please enter a description for this tournament (optional): ")
    all_data = {
                "tournament_name": f"{tournament_name}", 
                "tournament_place": f"{tournament_place}",
                "tournament_beginning_date": f"{tournament_beginning_date}",
                "tournament_end_date": f"{tournament_end_date}",
                "tournament_description": f"{tournament_description}",
                "number_of_rounds": f"{tournament_number_of_rounds}"
                }
    return all_data

def tournament_participants_input(nb_of_participants):
    counter = 0
    players = []
    print(
          "Add players to the new tournament. Players must be written in the following format: "
          "surname, name, national_chess_id"
         )
    while counter != nb_of_participants:
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
        print((f"{match[0]["player_surname"]} "
               f"{match[0]["player_name"]} "
               f"{match[0]["player_chess_national_id"]} "
               "vs "
               f"{match[1]["player_surname"]} "
               f"{match[1]["player_name"]} "
               f"{match[1]["player_chess_national_id"]}"))
        
def get_round_results(matches):
    print("Would you like to add results to these matches? Y/N")
    choice = input(">>> ")
    if choice == "Y":
        matches_result_list = []
        for match in matches:
            print((f"{match[0]["player_surname"]} "
               f"{match[0]["player_name"]} "
               f"{match[0]["player_chess_national_id"]} "
               "vs "
               f"{match[1]["player_surname"]} "
               f"{match[1]["player_name"]} "
               f"{match[1]["player_chess_national_id"]}"))
            print("Please enter winner's id or type 'draw'")
            result = input(">>> ")
            matches_result_list.append(result)
        return matches_result_list
    else:
        return None

