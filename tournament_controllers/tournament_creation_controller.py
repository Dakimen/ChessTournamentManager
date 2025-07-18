from views.tournament_views import tournament_data_input, tournament_participants_input
from models.tournament_models import Tournament
from models.player_models import Player, check_if_in_db
from views.player_menu_views import entered_correctly, get_date_of_birth

def manage_create_tournament():
    tournament_data = tournament_data_input()
    nb_players = calculate_number_of_players(tournament_data["number_of_rounds"])
    players_raw_input = tournament_participants_input(nb_players)
    players = get_tournament_players(players_raw_input)
    new_tournament = Tournament(tournament_data, players)
    new_tournament.save_tournament()

def calculate_number_of_players(nb_rounds):
    if nb_rounds == "":
        nb_rounds = 4
    else:
        nb_rounds = int(nb_rounds)
    nb_players = nb_rounds + 1 #In a round-robin where everyone plays 1 game per round and plays each opponent once per tournament
    return nb_players

def handle_not_in_db(new_player):
    correct = entered_correctly(new_player)
    if correct is False:
        new_player_date_of_birth = get_date_of_birth()
        new_player["date_of_birth"] = new_player_date_of_birth
        unreg_player = Player(new_player)
        unreg_player.save_player()
    else:
        return False

def get_tournament_players(players_raw_input):
    tournament_players = []
    for player in players_raw_input:
        player_segments = player.split(", ") #Splits into three parts: Surname, Name, ID
        new_player = {"player_surname": player_segments[0], "player_name": player_segments[1], "chess_national_id": player_segments[2]}
        if check_if_in_db(new_player) is False:
            handle_not_in_db(new_player)
        tournament_players.append(new_player)
    return tournament_players