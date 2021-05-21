import json
from datetime import datetime


class Tournament:
    def __init__(
        self,
        name,
        place,
        start_date,
        end_date,
        time_control,
        description,
        rounds=[],
        players=[],
        nb_of_rounds=4,
    ):

        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.time_control = time_control
        self.description = description
        self.rounds = rounds
        self.players = players
        self.nb_of_rounds = nb_of_rounds

    @classmethod
    def create_tournament(cls):
        name = input("Name: ")
        place = input("Place: ")
        start_date = input("Start date: ")
        end_date = input("End date: ")
        time_control = input("Time control: ")
        description = input("Description ")
        return Tournament(name, place, start_date, end_date, time_control, description)

    def create_first_round(self):
        for player in self.players:
            print(int(player[0]))
        self.players = sorted(self.players, key=lambda player: player.ranking)


class Player:
    def __init__(self, first_name, last_name, date_of_birth, gender, ranking, score=0):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.ranking = ranking
        self.score = score

    @classmethod
    def create_player(cls):
        first_name = input("First name : ")
        last_name = input("Last_name : ")
        date_of_birth = input("Date_of_birth (yyyy/mm/dd) : ")
        gender = input("Gender: ")
        ranking = int(input("Ranking : "))
        return Player(first_name, last_name, date_of_birth, gender, ranking)

    def sort_player_by_ranking(self, list):
        return sorted(list, key=lambda player: player["ranking"])

    def sort_player_by_score(self, list):
        return sorted(
            list, key=lambda player: (player["score"], -player["ranking"]), reverse=True
        )

    def make_list_of_players_by_ranking(self, list):
        sort_list_of_players = []
        top_list_of_players = []
        down_list_of_players = []
        list_of_players_ordered = (top_list_of_players, down_list_of_players)
        sort_list_of_players = Player.sort_player_by_ranking(self, list)
        j = int(len(sort_list_of_players) / 2)
        for i in range(int(len(sort_list_of_players) / 2)):
            down_list_of_players.append(sort_list_of_players.pop(j))
            top_list_of_players.append(sort_list_of_players.pop(0))
            j -= 1
        return list_of_players_ordered

    def make_list_of_players_by_score(self, list):
        sort_list_of_players = []
        top_list_of_players = []
        down_list_of_players = []
        list_of_players_ordered = (top_list_of_players, down_list_of_players)
        sort_list_of_players = Player.sort_player_by_score(self, list)
        j = int(len(sort_list_of_players) / 2)
        for i in range(int(len(sort_list_of_players) / 2)):
            down_list_of_players.append(sort_list_of_players.pop(j))
            top_list_of_players.append(sort_list_of_players.pop(0))
            j -= 1
        return list_of_players_ordered


class Match:
    def __init__(self, player_1, player_2, score_player_1=0, score_player_2=0):
        self.match = ([player_1, score_player_1], [player_2, score_player_2])


class Round:
    def __init__(
        self, name, start_date, current_round, end_date=None, list_of_match=[]
    ):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.list_of_match = list_of_match
        self.current_round = current_round

    @classmethod
    def create_round(cls):
        current_round = 1
        name = "Round " + str(current_round)
        start_date = json.dumps(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        return Round(name, start_date, current_round)
