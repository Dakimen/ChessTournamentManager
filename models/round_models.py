#import storage_config
from datetime import datetime
import random

class Round:
    def generate_matches(self):
        raise NotImplementedError("This function must be implemented in the subclasses")
    def finish_round(self):
        self.finished = True
        self.end_date = datetime.now().strftime("%H:%M on %d/%m/%Y")


class FirstRound(Round):
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.finished = False
        time = datetime.now()
        self.start_date = time.strftime("%H:%M on %d/%m/%Y")
        self.end_date = 0

    def generate_matches(self):
        random.shuffle(self.players)
        generated_matches = list(zip(self.players[::2], self.players[1::2]))
        self.matches = generated_matches

    def finish_round(self):
         super().finish_round()

class SubsequentRound(Round):
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.finished = False
        time = datetime.now()
        self.start_date = time.strftime("%H:%M on %d/%m/%Y")
        self.end_date = 0

    def generate_matches(self):
        pass

    def finish_round(self):
         super().finish_round()




