import storage_config
from tinydb import Query
from models import round_models
from models.player_models import Tournament_Player
from models.round_models import FirstRound, SubsequentRound

class Tournament:
    """
    Tournament class, requires:
      1. tournament_data dictionary that includes:
      keys-values of tournament_name, tournament_place, tournament_beginning_date, tournament_end_date and number_of_rounds.
      2. A list of players
    """
    def __init__(self, tournament_data, players, rounds = []):
        self.name = tournament_data["tournament_name"]
        self.place = tournament_data["tournament_place"]
        self.dates = f"{tournament_data["tournament_beginning_date"]} - {tournament_data["tournament_end_date"]}"
        self.description = tournament_data["tournament_description"]
        if tournament_data["number_of_rounds"] == "":
            self.number_of_rounds = 4
        else:
            self.number_of_rounds = int(tournament_data["number_of_rounds"])
        self.str_players = []
        for each_player in players:
            new_str_player = each_player.stringify_self()
            self.str_players.append(new_str_player)
        self.players_list = []
        for each_player in players:
            new_tournament_player = Tournament_Player(each_player)
            self.players_list.append(new_tournament_player)
        self.rounds = []
        self.bye_history = [] 
        self.match_history = []
        if rounds != []:
          for round in rounds:
              self.rounds.append(round)

    def generate_round(self):
        new_round = None
        if len(self.rounds) == 0:
            new_round = round_models.FirstRound(self.players_list)
            new_round.generate_matches()
            self.rounds.append(new_round)
            self.bye_history.append(new_round.get_bye_player())
        else:
            n = len(self.rounds)
            new_round = round_models.SubsequentRound(f"Round {n}", self.players_list,
                                                      self.match_history, self.bye_history)
            new_round.generate_matches()
            self.rounds.append(new_round)

    def stringify_rounds(self):
        stringified_rounds = []
        for round in self.rounds:
            round_strings = round.stringify_matches()
            bye_player = round.get_bye_player()
            if bye_player != None:
                round_strings.append((f"{bye_player.player.surname} " 
                                      f"{bye_player.player.name} " 
                                      f"{bye_player.player.chess_national_id} "
                                      "did not participate in this round"))
            stringified_rounds.append(round_strings)
        return stringified_rounds

    def save_tournament(self):
        """Saves the tournament to the database"""
        round_dict = []
        for round in self.rounds:
            round_dict.append(round.get_data())
        storage_config.TOURNAMENT_DB.insert({
            "name": self.name,
            "place": self.place,
            "dates": self.dates,
            "description": self.description,
            "number_of_rounds": self.number_of_rounds,
            "players_list_raw": self.str_players,
            "rounds": round_dict
        })

def get_all_tournaments():
    all_tournaments = storage_config.TOURNAMENT_DB.all()
    return all_tournaments

def find_tournament(name, place):
    tournament = Query()
    found_tournament_by_name = storage_config.TOURNAMENT_DB.search(tournament.name == name)
    tournaments_in_place = storage_config.TOURNAMENT_DB.search(tournament.place == place)
    for tournament in found_tournament_by_name:
        if tournament in tournaments_in_place:
            return tournament
    else:
        return None
    
def recreate_tournament_input(tourn_dict):
    dates = tourn_dict["dates"]
    dates = dates.split(" - ")
    beginning_date = dates[0]
    end_date = dates[1]
    tourn_data = {
        "tournament_name": tourn_dict["name"],
        "tournament_place": tourn_dict["place"],
        "tournament_beginning_date": beginning_date,
        "tournament_end_date": end_date,
        "tournament_description": tourn_dict["description"],
        "number_of_rounds": tourn_dict["number_of_rounds"]
    }
    return tourn_data

