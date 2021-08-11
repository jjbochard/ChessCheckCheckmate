import json
from datetime import datetime

import input_validators


class Tournament:
    def __init__(
        self,
        name,
        place,
        time_control,
        description,
        status_tournament,
        start_date=json.dumps(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
        end_date=None,
        rounds=[],
        players=[],
        nb_of_rounds=4,
    ):

        self.name = name
        self.place = place
        self.time_control = time_control
        self.description = description
        self.status_tournament = status_tournament
        self.start_date = start_date
        self.end_date = end_date
        self.rounds = rounds
        self.players = players
        self.nb_of_rounds = nb_of_rounds

    @classmethod
    def create_tournament(cls):
        while True:
            name = input("Name: ").capitalize()
            if input_validators.is_tournament_already_exist(name):
                break
        place = input("Place: ").capitalize()
        while True:
            time_control = input("Time control (Biltz, Bullet or Rapid): ").capitalize()
            if input_validators.is_valid_time_control(time_control):
                break
        description = input("Description: ").capitalize()
        status_tournament = "pending"
        return Tournament(name, place, time_control, description, status_tournament)

    @classmethod
    def tournament_table_is_empty(cls, table):
        status_tournament_table = table.all()
        if status_tournament_table == []:
            return True

    @classmethod
    def status_tournament_is_finished(cls, table):
        status_tournament = table.all()[-1]["status_tournament"]
        if status_tournament == "finished":
            return True

    @staticmethod
    def get_tournaments(table):
        list_tournaments = []
        for tournament in table:
            tournament = str(tournament.doc_id)
            list_tournaments.append(tournament)
        return list_tournaments

    @staticmethod
    def get_tournament_name(table):
        return [tournament["name"] for tournament in table]

    @staticmethod
    def check_tournament_duplicate(tournament_name_one, tournament_name_two):
        if tournament_name_one == tournament_name_two:
            return True
