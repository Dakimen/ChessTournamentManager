import storage_config
from tinydb import Query
from models.player_models import Tournament_Player, Player
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
        self.players_list = []
        n = 0
        while n < len(players):
            if isinstance(players[n], Player):
                new_tournament_player = Tournament_Player(players[n], n)
                self.players_list.append(new_tournament_player)
            else:
                new_tournament_player = Tournament_Player(players[n][0], players[n][1], players[n][2])
                self.players_list.append(new_tournament_player)
            n += 1
        for each_player in self.players_list:
            new_str_player = each_player.stringify_self()
            self.str_players.append(new_str_player)
        self.rounds = []
        self.match_history = []
        if rounds != []:
          for round in rounds:
              self.rounds.append(round)

    def get_removed_list(self):
        removed_list = []
        for round in self.rounds:
            for player in self.players_list:
                if isinstance(round.removed_player, int):
                    if player.tournament_id == round.removed_player:
                        removed_list.append(player)
                elif isinstance(round.removed_player, Tournament_Player):
                    if player.tournament_id == round.removed_player.tournament_id:
                        removed_list.append(player)
                else:
                    raise f"removed_player is an incorrect instance {type(round.removed_player)}"
        return removed_list

    def generate_round(self):
        if len(self.rounds) < self.number_of_rounds:
            if len(self.rounds) == 0:
                new_round = FirstRound(self.players_list)
                new_round.generate_matches()
                self.rounds.append(new_round)
            else:
                self.get_match_history()
                match_history = self.match_history
                removed_list = self.get_removed_list()
                n = len(self.rounds) + 1
                new_round = SubsequentRound(f"Round {n}", self.players_list, n)
                new_round.generate_matches(match_history, removed_list)
                self.rounds.append(new_round)
        else: return None

    def stringify_rounds(self):
        stringified_rounds = []
        for round in self.rounds:
            round_strings = round.stringify_matches()
            stringified_rounds.append(round_strings)
        return stringified_rounds
    
    def get_current_round(self):
        for round in self.rounds:
            if round.finished == False:
                current_round = round
        return current_round

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

    def get_match_history(self):
        matches = []
        for round in self.rounds:
            for match in round.matches:
                match_tup = (match[0].tournament_id, match[1].tournament_id)
                print(match_tup)
                matches.append(match_tup)
        self.match_history = matches


def get_all_tournaments():
    all_tournaments = storage_config.TOURNAMENT_DB.all()
    return all_tournaments

def find_tournament(name, dates):
    tournament = Query()
    found_tournament_by_name = storage_config.TOURNAMENT_DB.search(tournament.name == name)
    tournaments_in_place = storage_config.TOURNAMENT_DB.search(tournament.dates == dates)
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

def get_round_in_db(tournament):
    tournament_in_db = Query()
    tournament_doc = storage_config.TOURNAMENT_DB.search(tournament_in_db.name == tournament.name)[0]
    tournament_id = tournament_doc.doc_id
    return tournament_id

def update_player_points_in_db(tournament = Tournament):
    tournament_id = get_round_in_db(tournament)
    tournament.str_players = []
    for player in tournament.players_list:
        str_player = player.stringify_self()
        tournament.str_players.append(str_player)
    storage_config.TOURNAMENT_DB.update({"players_list_raw": tournament.str_players}, doc_ids = [tournament_id])

def mark_round_finished(current_round, tournament):
    current_round.finish_round()
    tournament_id = get_round_in_db(tournament)
    updated_rounds = []
    for round in tournament.rounds:
        upd_round = round.get_data()
        updated_rounds.append(upd_round)
    storage_config.TOURNAMENT_DB.update({"rounds": updated_rounds}, doc_ids = [tournament_id])

