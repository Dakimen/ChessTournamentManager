import storage_config
import round_models

class Tournament:
    """
    Tournament class, requires:
      1. tournament_data dictionary that includes:
      keys-values of tournament_name, tournament_place, tournament_beginning_date, tournament_end_date and number_of_rounds.
      2. A list of players
    """
    def __init__(self, tournament_data, players):
        self.name = tournament_data["tournament_name"]
        self.place = tournament_data["tournament_place"]
        self.dates = f"{tournament_data["tournament_beginning_date"]} - {tournament_data["tournament_end_date"]}"
        self.description = tournament_data["tournament_description"]
        if tournament_data["number_of_rounds"] == "":
            self.number_of_rounds = 4
        else:
            self.number_of_rounds = int(tournament_data["number_of_rounds"])
        self.players_list = players
        self.rounds = []
        self.match_history = []
        self.bye_history = [] #In case the player number is uneven and each player needs to skip one round

    def generate_round(self):
        new_round = None
        if len(self.rounds) == 0:
            new_round = round_models.FirstRound("Round 1", self.players_list)
            new_round.generate_matches()
            self.rounds.append(new_round)
        else:
            n = len(self.rounds)
            new_round = round_models.SubsequentRound(f"Round {n}", self.players_list, self.match_history, self.bye_history)
            new_round.generate_matches()
            self.rounds.append(new_round)

    def save_tournament(self):
        """Saves the tournament to the database"""
        storage_config.TOURNAMENT_DB.insert({
            "name": self.name,
            "place": self.place,
            "dates": self.dates,
            "description": self.description,
            "number_of_rounds": self.number_of_rounds,
            "players_list_raw": self.players_list,
            "rounds": self.rounds
        })
        
