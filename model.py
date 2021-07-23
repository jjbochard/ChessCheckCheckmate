import json
import random
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
        name = input("Name: ").capitalize()
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


class Player:
    def __init__(
        self, first_name, last_name, date_of_birth, gender, ranking, score=0.0
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.ranking = ranking
        self.score = score

    @classmethod
    def create_player(cls):
        while True:
            first_name = input("First name : ").capitalize()
            last_name = input("Last_name : ").capitalize()
            date_of_birth = input_validators.is_valid_date_of_birth()
            if input_validators.is_not_already_added_player(
                first_name, last_name, date_of_birth
            ):
                break
        while True:
            gender = input("Gender (Female or Male): ").capitalize()
            if input_validators.is_valid_gender(gender):
                break
        while True:
            ranking = int(input("Ranking : "))
            if input_validators.is_unused_ranking(ranking):
                break
        return Player(first_name, last_name, date_of_birth, gender, ranking)

    @staticmethod
    def get_players(table):
        list_players = []
        for player in table:
            player = player.doc_id
            list_players.append(player)
        return list_players

    @staticmethod
    def get_rankings(table):
        return [player["ranking"] for player in table]

    @staticmethod
    def get_full_name_and_date_of_birth(table):
        list_full_name = []
        list_date_of_birth = []
        for player in table:
            full_name = "%s %s" % (player["first_name"], player["last_name"])
            date_of_birth = player["date_of_birth"]
            list_full_name.append(full_name)
            list_date_of_birth.append(date_of_birth)
        return list_full_name, list_date_of_birth

    @staticmethod
    def check_full_name_duplicate(
        current_full_name, list_full_name, list_date_of_birth
    ):
        full_name_duplicate = []
        date_of_birth_of_full_name_duplicate = []
        for index, full_name in enumerate(list_full_name):
            if full_name == current_full_name:
                full_name_duplicate.append(full_name)
                date_of_birth_of_full_name_duplicate.append(list_date_of_birth[index])
        return date_of_birth_of_full_name_duplicate

    @staticmethod
    def check_date_duplicate(date_one, date_two):
        if date_one == date_two:
            return True

    def sort_player_by_ranking(self, list):
        return sorted(list, key=lambda player: player["ranking"])

    def sort_player_by_score(self, list):
        return sorted(
            list, key=lambda player: (player["score"], -player["ranking"]), reverse=True
        )

    def sort_list_of_players_by_ranking(self, list):
        sort_list_of_players = []
        top_list_of_players = []
        down_list_of_players = []
        list_of_players_ordered = (top_list_of_players, down_list_of_players)
        sort_list_of_players = Player.sort_player_by_ranking(self, list)
        j = int(len(sort_list_of_players) / 2)
        for _ in range(int(len(sort_list_of_players) / 2)):
            down_list_of_players.append(sort_list_of_players.pop(j))
            top_list_of_players.append(sort_list_of_players.pop(0))
            j -= 1
        return list_of_players_ordered

    def sort_list_of_players_by_score(self, list):
        list_of_players_ordered = []
        list_of_players_ordered = Player.sort_player_by_score(self, list)
        return list_of_players_ordered

    def update_score_player(self, match, response, table):
        if response == "1":
            table.update(
                {"score": table.all()[(match["player_1"]) - 1]["score"] + 1.0},
                doc_ids=[(table.all()[(match["player_1"]) - 1]).doc_id],
            )
            table.update(
                {"score": table.all()[(match["player_2"]) - 1]["score"] + 0.0},
                doc_ids=[(table.all()[(match["player_2"]) - 1]).doc_id],
            )
        if response == "2":
            table.update(
                {"score": table.all()[(match["player_1"]) - 1]["score"] + 0.0},
                doc_ids=[(table.all()[(match["player_1"]) - 1]).doc_id],
            )
            table.update(
                {"score": table.all()[(match["player_2"]) - 1]["score"] + 1.0},
                doc_ids=[(table.all()[(match["player_2"]) - 1]).doc_id],
            )
        if response == "3":
            table.update(
                {"score": table.all()[(match["player_1"]) - 1]["score"] + 0.5},
                doc_ids=[(table.all()[(match["player_1"]) - 1]).doc_id],
            )
            table.update(
                {"score": table.all()[(match["player_2"]) - 1]["score"] + 0.5},
                doc_ids=[(table.all()[(match["player_2"]) - 1]).doc_id],
            )

    def list_of_remaining_players(self, table):
        return [
            [
                player.doc_id,
                player["last_name"],
                player["first_name"],
                player["ranking"],
                player["date_of_birth"],
                player["gender"],
            ]
            for player in table
        ]

    def initialize_score(self, player_table, tournament_table):
        for player in tournament_table.all()[-1]["players"]:
            player_table.update(
                {"score": 0.0},
                doc_ids=[player_table.all()[player - 1].doc_id],
            )


class Match:
    def __init__(self, player_1, player_2, score_player_1=0, score_player_2=0):
        self.player_1 = player_1
        self.player_2 = player_2
        self.score_player_1 = score_player_1
        self.score_player_2 = score_player_2

    @classmethod
    def create_match(cls, random_player_1, random_player_2):
        generate_color = random.randrange(2)
        if generate_color == 0:
            player_1 = random_player_1
            player_2 = random_player_2
        else:
            player_1 = random_player_2
            player_2 = random_player_1
        return Match(player_1, player_2)

    def update_score_match(self, match, response, table):
        if response == "1":
            table.update(
                {"score_player_1": 1.0},
                doc_ids=[match.doc_id],
            )
            table.update(
                {"score_player_2": 0.0},
                doc_ids=[match.doc_id],
            )
        elif response == "2":
            table.update(
                {"score_player_1": 0.0},
                doc_ids=[match.doc_id],
            )
            table.update(
                {"score_player_2": 1.0},
                doc_ids=[match.doc_id],
            )
        elif response == "3":
            table.update(
                {"score_player_1": 0.5},
                doc_ids=[match.doc_id],
            )
            table.update(
                {"score_player_2": 0.5},
                doc_ids=[match.doc_id],
            )


class Round:
    def __init__(
        self,
        name,
        start_date,
        current_round,
        status_round,
        end_date=None,
        list_of_match=[],
    ):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.list_of_match = list_of_match
        self.current_round = current_round
        self.status_round = status_round

    @classmethod
    def create_round(cls):
        current_round = 1
        name = "Round " + str(current_round)
        start_date = json.dumps(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        status_round = "pending"
        return Round(name, start_date, current_round, status_round)

    def end_round(round_table):
        round_table.update(
            {"status_round": "finished"},
            doc_ids=[round_table.all()[-1].doc_id],
        )
        round_table.update(
            {
                "end_date": json.dumps(
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S"), default=str
                )
            },
            doc_ids=[round_table.all()[-1].doc_id],
        )
