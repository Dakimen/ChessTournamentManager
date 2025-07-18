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

def entered_correctly(new_player):
    print(f"{new_player["player_name"]} {new_player["player_surname"]} doesn't appear to be in the database.")
    sure = ""
    while sure != "Y" or sure != "N":
        sure = input("Are you sure their information was entered correctly? (Y/N): ")
        if sure == "N":
            return False
        elif sure == "Y":
            return True
        
def get_date_of_birth():
    date_of_birth = input("Please enter their date of birth: ")
    return date_of_birth