import random


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
