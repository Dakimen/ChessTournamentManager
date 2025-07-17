class Menu:
    def __init__(self, menu_name, options):
        self.options = []
        self.option_keys = []
        for option in options:
            self.options.append(option)
            self.option_keys.append(options[option])
        self.menu_name = menu_name
        
    def display_menu(self):
        print((
           f"{self.menu_name}"
           ))
        ticker = 0
        for option in self.options:
            print(f"{self.option_keys[ticker]}: {option}")
            ticker = ticker + 1
        user_choice = input(">>> ")
        if user_choice not in self.option_keys:
            while user_choice not in self.option_keys:
                print("Please insert a valid option")
                user_choice = input(">>> ")
        return user_choice

def player_addition_view():
    new_player_name = input("Insert new player's name: ")
    new_player_surname = input("Insert new player's surname: ")
    new_player_date_of_birth = input("Insert new player's date of birth: ")
    new_player_national_chess_id = input("Insert new player's national chess ID: ")
    new_player_player_info = {
                   "player_name": f"{new_player_name}", "player_surname": f"{new_player_surname}",
                   "date_of_birth": f"{new_player_date_of_birth}", "chess_national_id": f"{new_player_national_chess_id}"
                   }
    return new_player_player_info

def display_list_of_players(list_of_players):
    for player in list_of_players:
        print(f"{player["name"]} {player["surname"]}, {player["date_of_birth"]}, {player["chess_national_id"]}")

def handle_false_id():
    print("ID you entered appears to be taken or incorrect.")
    print("A valid ID must contain two capital letters followed by 5 numbers in this format: "
          "AB00000")
    new_id = input("Please enter a valid ID: ")
    return new_id 
          
def tournament_data_input():
    print("Please enter new tournament information")
    tournament_name = input("Please enter the name of the new tournament: ")
    tournament_place = input("Please enter where this tournament will take place: ")
    tournament_beginning_date = input("Please enter the start date of the tournament: ")
    tournament_end_date = input("Please enter the end date of this tournament: ")
    tournament_number_of_rounds = input("Please enter the number of rounds to take place (optional, defaults to 4): ")
    tournament_registered_players_surnames = input("Please enter the surnames of players scheduled to participate: ")
    tournament_description = input("Please enter a description for this tournament (optional): ")
    all_data = {
                "tournament_name": f"{tournament_name}", 
                "tournament_place": f"{tournament_place}",
                "tournament_beginning_date": f"{tournament_beginning_date}",
                "tournament_end_date": f"{tournament_end_date}",
                "tournament_registered_players_surnames": f"{tournament_registered_players_surnames}",
                "tournament_description": f"{tournament_description}"}
    if tournament_number_of_rounds is not "":
        all_data["number_of_rounds"] = tournament_number_of_rounds
    return all_data
