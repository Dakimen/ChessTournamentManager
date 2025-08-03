import re


class PlayerView:
    def __init__(self):
        self.names_format = re.compile(r"^[A-Z][a-z]*(?:[-'][A-Z][a-z]*)*")
        self.numbers_format = re.compile(r"^[0-9]{2}$")
        self.date_format = re.compile(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$")
        self.id_format = re.compile(r"[A-Z]{2}[0-9]{5}$")
        self.year_format = re.compile(r"^[0-9]{4}$")

    def player_addition_view(self):
        new_player_name = input("Insert new player's name: ")
        while not self.names_format.fullmatch(new_player_name):
            print("Please avoid using any characters other than letters, commas and apostrophes")
            print("Also please make sure that the first letter is capitalized")
            new_player_name = input("Insert new player's name: ")
        new_player_surname = input("Insert new player's surname: ")
        while not self.names_format.fullmatch(new_player_surname):
            print("Please avoid using any characters other than letters, commas and apostrophes")
            print("Also please make sure that the first letter is capitalized")
            new_player_surname = input("Insert new player's surname: ")
        new_player_date_of_birth = input("Insert new player's date of birth in a dd/mm/yyyy format: ")
        while not self.date_format.fullmatch(new_player_date_of_birth):
            print("Please use the dd/mm/yyyy format.")
            new_player_date_of_birth = input("Insert new player's date of birth in a dd/mm/yyyy format: ")
        new_player_national_chess_id = input("Insert new player's "
                                             "national chess ID using ID00000 format: ")
        while not self.id_format.fullmatch(new_player_national_chess_id):
            print("Please use the ID00000 format.")
            new_player_national_chess_id = input("Insert new player's "
                                                 "national chess ID using ID00000 format: ")
        new_player_player_info = {
                       "player_name": f"{new_player_name}",
                       "player_surname": f"{new_player_surname}",
                       "date_of_birth": f"{new_player_date_of_birth}",
                       "chess_national_id": f"{new_player_national_chess_id}"
                       }
        return new_player_player_info
    
    def get_data(self, id):
        print(f"Player {id['chess_national_id']} doesn't seem to be in the database. Let's fix that.")
        name = input("Please enter their name: ")
        while not self.names_format.fullmatch(name):
            print("Please avoid using anything but letters, commas, dashes and apostrophes.")
            print("Also please make sure the name starts with a capitalized letter.")
            name = input("Please enter their name: ")
        surname = input("Please enter their surname: ")
        while not self.names_format.fullmatch(surname):
            print("Please avoid using anything but letters, commas, dashes and apostrophes.")
            print("Also please make sure the name starts with a capitalized letter.")
            surname = input("Please enter their surname: ")
        date_of_birth = input("Please enter their date of birth in the yyyy format: ")
        while not self.year_format.fullmatch(date_of_birth):
            print("Please follow the yyyy format.")
            date_of_birth = input("Please enter their date of birth in the yyyy format: ")
        return {
            "player_name": name,
            "player_surname": surname,
            "date_of_birth": date_of_birth,
            "chess_national_id": id["chess_national_id"]
        }
    
    def handle_false_id(self):
        new_id = None
        while not self.id_format.fullmatch(new_id):
            print("ID you entered appears to be taken or incorrect.")
            print("A valid ID must contain two capital letters "
                  "followed by 5 numbers in this format: "
                  "AB00000")
            new_id = input("Please enter a valid ID: ")
        return new_id

    @staticmethod
    def display_list_of_players(list_of_players):
        for player in list_of_players:
            print(f"{player.surname} {player.name}, "
                  f"{player.date_of_birth}, {player.chess_national_id}")

