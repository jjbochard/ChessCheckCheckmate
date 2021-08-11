import input_validators


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

    def read_players(self):

        players = [
            [
                player["ranking"],
                player.doc_id,
                player["last_name"],
                player["first_name"],
                player["date_of_birth"],
                player["gender"],
            ]
            for player in self.player_table
        ]

        players = sorted(players)
        return players

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
