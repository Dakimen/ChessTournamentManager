from views.tournament_views import (
     tournament_data_input, tournament_participants_input
     )
from models.tournament_models import Tournament
from models.player_models import Player, check_if_in_db, get_player_from_db
from views.player_menu_views import get_date_of_birth


def manage_create_tournament():
    tournament_data = tournament_data_input()
    n_of_rounds = tournament_data["number_of_rounds"]
    nb_players = calculate_number_of_players(n_of_rounds)
    players_raw_input = tournament_participants_input(nb_players)
    players = get_tournament_players(players_raw_input)
    new_tournament = Tournament(tournament_data, players)
    new_tournament.generate_round()
    new_tournament.save_tournament()


def calculate_number_of_players(nb_rounds):
    if nb_rounds == "":
        nb_rounds = 4
    else:
        nb_rounds = int(nb_rounds)
    nb_players = nb_rounds + 1
    return nb_players


def handle_not_in_db(new_player):
    new_player_date_of_birth = get_date_of_birth()
    new_player["date_of_birth"] = new_player_date_of_birth
    unreg_player = Player(new_player)
    unreg_player.save_player()
    return unreg_player


def get_tournament_players(players_raw_input):
    tournament_players = []
    for player in players_raw_input:
        player_segments = player.split(", ")
        new_player = {"player_surname": player_segments[0],
                      "player_name": player_segments[1],
                      "chess_national_id": player_segments[2]}
        if check_if_in_db(new_player) is False:
            unreg_player = handle_not_in_db(new_player)
            tournament_players.append(unreg_player)
        else:
            reg_player_data = get_player_from_db(new_player)
            reg_player = Player(reg_player_data)
            tournament_players.append(reg_player)
    return tournament_players
