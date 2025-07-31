from tinydb import TinyDB
from tinydb.storages import JSONStorage

class PrettyJSONStorage(JSONStorage):
    def __init__(self, *args, **kwargs):
        kwargs['indent'] = 4
        super().__init__(*args, **kwargs)

PLAYER_DB = TinyDB("player_database.json", storage = PrettyJSONStorage)
TOURNAMENT_DB = TinyDB("tournament_database.json", storage = PrettyJSONStorage)