from tinydb import TinyDB


class View:
    def __init__(self, db, tournament_table):
        self.db = TinyDB("db.json")
        self.tournament_table = db.table("tournament")
