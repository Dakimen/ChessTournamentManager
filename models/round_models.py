#import storage_config
from datetime import datetime

class Round:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.finished = False
        time = datetime.now()
        self.start_date = time.strftime("%H:%M on %d/%m/%Y")
        self.end_date = 0
    
    def finish_round(self):
        self.finished = True
        self.end_date = datetime.now().strftime("%H:%M on %d/%m/%Y")



