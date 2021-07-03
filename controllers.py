import collections
import json
from datetime import datetime

from tinydb import Query, TinyDB

import input_validators
from model import Match, Player, Round, Tournament


class Controller:
    def __init__(
        self,
        select,
        table,
        warning,
        tournament_table=TinyDB("db.json").table("tournament"),
        player_table=TinyDB("db.json").table("player"),
        round_table=TinyDB("db.json").table("round"),
        match_table=TinyDB("db.json").table("match"),
    ):
        self.select = select
        self.table = table
        self.warning = warning
        self.tournament_table = tournament_table
        self.player_table = player_table
        self.round_table = round_table
        self.match_table = match_table

    def run(self):
        """
        Loop that runs all the next
        'menu' methods from the controllers
        """
        self.warning.welcome_message()
        self.main_menu()

    def main_menu(self):
        """ """
        while True:
            response = self.select.main_menu()
            if input_validators.is_valid_main_menu_response(response):
                break
        if response == "1":
            if (
                self.tournament_table.all() == []
                or self.tournament_table.all()[-1]["status_tournament"] == "finished"
            ):
                return self.create_tournament()
            else:
                return self.continue_tournament()
        if response == "2":
            return self.create_player()
        if response == "3":
            return self.display_change_ranking_menu()
        if response == "4":
            return self.display_tournaments_menu()
        if response == "5":
            return self.display_players_menu()
        if response == "6":
            return self.quit()

    def display_tournaments_menu(self):
        """ """
        response = self.table.tournaments()
        while True:
            response = self.select.tournament_menu()
            if input_validators.is_valid_tournament_menu_response(response):
                break

        if response == "1":
            return self.display_choice_tournament_for_print_players()
        if response == "2":
            return self.display_choice_tournament_for_print_rounds()
        if response == "3":
            return self.display_choice_tournament_for_print_matchs()
        if response == "4":
            return self.display_change_ranking_menu()
        if response == "5":
            return self.main_menu()
        if response == "6":
            return self.quit()

    def display_choice_tournament_for_print_players(self):
        """ """
        choice_tournament = self.select.choose_tournament_for_print_players()
        while True:
            choice_manner = self.select.print_players_menu()
            if input_validators.is_valid_print_players_menu_response(choice_manner):
                break
        if choice_manner == "1":
            self.table.players_by_ranking_of_tournament(choice_tournament)
        else:
            self.table.players_by_alphabetical_order_of_tournament(choice_tournament)
        self.display_tournaments_menu()

    def display_choice_tournament_for_print_rounds(self):
        """ """
        choice_tournament = self.select.choose_tournament_for_print_rounds()
        self.table.rounds_of_tournament(choice_tournament)
        self.display_tournaments_menu()

    def display_choice_tournament_for_print_matchs(self):
        """ """
        choice_tournament = self.select.choose_tournament_for_print_matchs()
        response = self.table.matchs_of_tournament(choice_tournament)
        while True:
            response = self.select.tournament_menu()
            if input_validators.is_valid_tournament_menu_response(response):
                break

        if response == "1":
            return self.display_choice_tournament_for_print_players()
        if response == "2":
            return self.display_choice_tournament_for_print_rounds()
        if response == "3":
            return self.display_choice_tournament_for_print_matchs()
        if response == "4":
            return self.display_change_ranking_menu()
        if response == "5":
            return self.main_menu()
        if response == "6":
            return self.quit()

    def display_players_menu(self):
        """ """
        while True:
            response = self.select.players_menu()
            if input_validators.is_valid_players_menu_response(response):
                break

        if response == "1":
            return self.display_players_by_ranking()
        if response == "2":
            return self.display_players_by_alphabetical_order()
        if response == "3":
            return self.display_change_ranking_menu()
        if response == "4":
            return self.main_menu()
        if response == "5":
            return self.quit()

    def update_score_match(self, match, response):
        if response == "1":
            self.match_table.update(
                {"score_player_1": 1.0},
                doc_ids=[match.doc_id],
            )
            self.match_table.update(
                {"score_player_2": 0.0},
                doc_ids=[match.doc_id],
            )
        elif response == "2":
            self.match_table.update(
                {"score_player_1": 0.0},
                doc_ids=[match.doc_id],
            )
            self.match_table.update(
                {"score_player_2": 1.0},
                doc_ids=[match.doc_id],
            )
        elif response == "3":
            self.match_table.update(
                {"score_player_1": 0.5},
                doc_ids=[match.doc_id],
            )
            self.match_table.update(
                {"score_player_2": 0.5},
                doc_ids=[match.doc_id],
            )

    def update_score_player(self, match, response):
        if response == "1":
            self.player_table.update(
                {
                    "score": self.player_table.all()[(match["player_1"]) - 1]["score"]
                    + 1.0
                },
                doc_ids=[(self.player_table.all()[(match["player_1"]) - 1]).doc_id],
            )
            self.player_table.update(
                {
                    "score": self.player_table.all()[(match["player_2"]) - 1]["score"]
                    + 0.0
                },
                doc_ids=[(self.player_table.all()[(match["player_2"]) - 1]).doc_id],
            )
        if response == "2":
            self.player_table.update(
                {
                    "score": self.player_table.all()[(match["player_1"]) - 1]["score"]
                    + 0.0
                },
                doc_ids=[(self.player_table.all()[(match["player_1"]) - 1]).doc_id],
            )
            self.player_table.update(
                {
                    "score": self.player_table.all()[(match["player_2"]) - 1]["score"]
                    + 1.0
                },
                doc_ids=[(self.player_table.all()[(match["player_2"]) - 1]).doc_id],
            )
        if response == "3":
            self.player_table.update(
                {
                    "score": self.player_table.all()[(match["player_1"]) - 1]["score"]
                    + 0.5
                },
                doc_ids=[(self.player_table.all()[(match["player_1"]) - 1]).doc_id],
            )
            self.player_table.update(
                {
                    "score": self.player_table.all()[(match["player_2"]) - 1]["score"]
                    + 0.5
                },
                doc_ids=[(self.player_table.all()[(match["player_2"]) - 1]).doc_id],
            )

    def update_scores(self, match):
        """ """
        while True:
            response = self.select.write_score_menu(match)
            if input_validators.is_valid_write_score_menu_response(response):
                break
        self.update_score_match(match, response)
        self.update_score_player(match, response)

    def display_players_by_ranking(self):
        """ """
        response = self.table.players_by_ranking()
        while True:
            response = self.select.players_by_ranking_menu()
            if input_validators.is_valid_players_by_ranking_menu_response(response):
                break

        if response == "1":
            return self.display_players_by_alphabetical_order()
        if response == "2":
            return self.display_change_ranking_menu()
        if response == "3":
            return self.main_menu()
        if response == "4":
            return self.quit()

    def display_players_by_alphabetical_order(self):
        """ """
        response = self.table.players_by_alphabetical_order()
        while True:
            response = self.select.players_by_alphabetical_order_menu()
            if input_validators.is_valid_players_by_alphabetical_order_menu_response(
                response
            ):
                break

        if response == "1":
            return self.display_players_by_ranking()
        if response == "2":
            return self.display_change_ranking_menu()
        if response == "3":
            return self.main_menu()
        if response == "4":
            return self.quit()

    def display_change_ranking_menu(self):
        self.table.players_by_id()
        while True:
            response = self.select.ranking_menu()
            if input_validators.is_valid_ranking_menu_response(response):
                break
        if response == "1":
            return self.change_ranking()
        if response == "2":
            return self.main_menu()

    def display_choice_create_next_round(self):
        while True:
            response = self.select.next_round_menu()
            if input_validators.is_valid_next_round_menu_response(response):
                break
        if response == "1":
            return self.create_round()
        if response == "2":
            return self.change_ranking()
        if response == "3":
            return self.main_menu()
        if response == "4":
            return self.quit()

    def display_choice_end_round(self):
        while True:
            response = self.select.end_round_menu()
            if input_validators.is_valid_end_round_menu_response(response):
                break
        if response == "1":
            return self.end_round()
        if response == "2":
            return self.main_menu()
        if response == "3":
            return self.quit()

    def quit(self):
        """
        Close the program
        """
        self.warning.quit()
        return True

    def create_tournament(self):
        new_tournament = Tournament.create_tournament()
        serialized_tournament = vars(new_tournament)
        self.tournament_table.insert(serialized_tournament)

        self.add_players_to_tournament()
        while self.tournament_table.all()[-1]["status_tournament"] != "finished":
            quit_before_create_round = self.display_choice_create_next_round()
            if quit_before_create_round is True:
                break
            quit_before_end_round = self.display_choice_end_round()
            if quit_before_end_round is True:
                break
            j = -4
            while j < 0:
                self.update_scores(self.match_table.all()[j])
                j += 1
            self.table.players_by_score()
            if self.round_table.all()[-1]["current_round"] == 4:
                self.create_end_tournament()

    def continue_tournament(self):
        while self.tournament_table.all()[-1]["status_tournament"] != "finished":
            if (
                self.round_table.all() == []
                or self.round_table.all()[-1]["status_round"] == "finished"
            ):
                quit_before_create_round = self.display_choice_create_next_round()
                if quit_before_create_round is True:
                    break
                quit_before_end_round = self.display_choice_end_round()
                if quit_before_end_round is True:
                    break
                j = -4
                while j < 0:
                    self.update_scores(self.match_table.all()[j])
                    j += 1
                self.table.players_by_score()
                if self.round_table.all()[-1]["current_round"] == 4:
                    self.create_end_tournament()

            else:
                quit_before_end_round = self.display_choice_end_round()
                if quit_before_end_round is True:
                    break

                j = -4
                while j < 0:
                    self.update_scores(self.match_table.all()[j])
                    j += 1
                self.table.players_by_score()
                if self.round_table.all()[-1]["current_round"] == 4:
                    self.create_end_tournament()
                else:
                    quit_before_create_round = self.display_choice_create_next_round()
                    if quit_before_create_round is True:
                        break

    def add_players_to_tournament(self):
        list_of_players = [1, 2, 3, 4, 5, 6, 7, 8]
        # number_of_player = 0
        # list_of_players_added = []
        # list_of_remaining_players = []
        # for player in self.player_table:
        #     list_of_remaining_players.append(
        #         [
        #             player.doc_id,
        #             player["last_name"],
        #             player["first_name"],
        #             player["ranking"],
        #             player["date_of_birth"],
        #             player["gender"],
        #         ]
        #     )
        # while number_of_player < 8:
        #     self.table.remaining_players(list_of_remaining_players)
        #     self.warning.remaining_players_to_add(number_of_player)
        #     while True:
        #         response = self.select.add_player_create_tournament_menu()
        #         if input_validators.is_valid_display_add_player_create_tournament_menu_response(
        #             response
        #         ):
        #             break
        #     if response == "1":
        #         existed_player_id = int(
        #             self.choice_player_for_add_player_to_a_tournament()
        #         )
        #         list_of_players_added.append(existed_player_id)
        #     elif response == "2":
        #         new_player_id = self.create_player()
        #         list_of_players_added.append(new_player_id)

        #     number_of_player += 1

        #     contains_duplicates = any(
        #         list_of_players_added.count(element) > 1
        #         for element in list_of_players_added
        #     )
        #     if contains_duplicates is True:
        #         list_of_players_added.pop(-1)
        #         number_of_player -= 1
        #         self.warning.add_a_player_several_time()
        #         continue

        #     tournament_table.update(
        #         {"players": list_of_players_added},
        #         doc_ids=[tournament_table.all()[-1].doc_id],
        #     )
        #     for player in tournament_table.all()[-1]["players"]:
        #         player_table.update(
        #             {"score": 0.0},
        #             doc_ids=[player_table.all()[player - 1].doc_id],
        #         )
        #     for player in list_of_remaining_players:
        #         if player[0] == existed_player_id:
        #             list_of_remaining_players.remove(player)
        self.tournament_table.update(
            {"players": list_of_players},
            doc_ids=[self.tournament_table.all()[-1].doc_id],
        )
        for player in self.tournament_table.all()[-1]["players"]:
            self.player_table.update(
                {"score": 0},
                doc_ids=[self.player_table.all()[player - 1].doc_id],
            )

    def create_player(self):
        new_player = Player.create_player()
        serialized_player = vars(new_player)
        self.player_table.insert(serialized_player)
        new_player_id = self.player_table.all()[-1].doc_id
        if (
            self.tournament_table.all()[-1]["status_tournament"] == "finished"
            or not self.tournament_table.all()
        ):
            return self.main_menu()
        else:
            return new_player_id

    def get_input_new_ranking(self):
        id_player = int(self.select.change_ranking())
        new_ranking = int(
            input(
                "Enter a new ranking for "
                + str(
                    self.player_table.all()[id_player - 1]["first_name"]
                    + " "
                    + str(self.player_table.all()[id_player - 1]["last_name"] + "\n")
                )
            )
        )
        self.player_table.update(
            {"ranking": new_ranking},
            doc_ids=[self.player_table.all()[id_player - 1].doc_id],
        )
        return new_ranking

    def check_same_ranking(self):
        players_ranking = []
        for player in self.player_table:
            players_ranking.append(player["ranking"])
        contains_duplicates = any(
            players_ranking.count(element) > 1 for element in players_ranking
        )
        return contains_duplicates

    def change_ranking(self):
        new_ranking = self.get_input_new_ranking()
        contains_duplicates = self.check_same_ranking()
        while contains_duplicates is True:
            self.table.players_by_id()
            self.warning.players_same_ranking(new_ranking)
            new_ranking = self.get_input_new_ranking()
            contains_duplicates = self.check_same_ranking()
        return self.display_change_ranking_menu()

    def end_round(self):
        self.round_table.update(
            {"status_round": "finished"},
            doc_ids=[self.round_table.all()[-1].doc_id],
        )
        self.round_table.update(
            {
                "end_date": json.dumps(
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S"), default=str
                )
            },
            doc_ids=[self.round_table.all()[-1].doc_id],
        )

    def create_round(self):
        new_round = Round.create_round()
        serialized_round = vars(new_round)
        if (
            self.round_table.all() == []
            or self.round_table.all()[-1]["current_round"] == 4
        ):
            self.round_table.insert(serialized_round)
            list_ranking_player = []
            new_matchs_id = []
            for player in self.tournament_table.all()[-1]["players"]:
                list_ranking_player.append((self.player_table.get(doc_id=player)))
            list_of_players_by_ranking = Player.make_list_of_players_by_ranking(
                self, list_ranking_player
            )
            Play = Query()
            for i in range(4):
                new_match = Match.create_match(
                    self.player_table.get(
                        Play.ranking == list_of_players_by_ranking[0][i]["ranking"]
                    ).doc_id,
                    self.player_table.get(
                        Play.ranking == list_of_players_by_ranking[1][i]["ranking"]
                    ).doc_id,
                )
                serialized_match = vars(new_match)
                self.match_table.insert(serialized_match)
                new_matchs_id.append(self.match_table.all()[-1].doc_id)
            list_of_rounds = self.tournament_table.all()[-1]["rounds"]
            list_of_rounds.append(self.round_table.all()[-1].doc_id)
            self.round_table.update(
                {"list_of_match": new_matchs_id},
                doc_ids=[self.round_table.all()[-1].doc_id],
            )
            self.tournament_table.update(
                {"rounds": list_of_rounds},
                doc_ids=[self.tournament_table.all()[-1].doc_id],
            )
            self.warning.round_create(str(self.round_table.all()[-1]["current_round"]))
            self.table.matchs()

        else:
            serialized_round["current_round"] = (
                self.round_table.all()[-1]["current_round"] + 1
            )
            serialized_round["name"] = "Round " + str(serialized_round["current_round"])

            self.round_table.insert(serialized_round)

            list_score_player = []
            new_matchs_id = []
            for player in self.tournament_table.all()[-1]["players"]:
                list_score_player.append((self.player_table.get(doc_id=player)))
            list_of_players_by_score = Player.make_list_of_players_by_score(
                self, list_score_player
            )
            all_matchs_of_a_tournament = []
            for rounds in self.tournament_table.all()[-1]["rounds"]:
                for matchs in self.round_table.all()[rounds - 1]["list_of_match"]:
                    all_matchs_of_a_tournament.append(
                        [
                            self.match_table.all()[matchs - 1]["player_1"],
                            self.match_table.all()[matchs - 1]["player_2"],
                        ]
                    )
            Play = Query()
            j = 0
            for i in range(4):
                k = 1
                exist = self.check_match_already_play(
                    all_matchs_of_a_tournament,
                    self.player_table.get(
                        Play.ranking == list_of_players_by_score[j]["ranking"]
                    ).doc_id,
                    self.player_table.get(
                        Play.ranking == list_of_players_by_score[j + 1]["ranking"]
                    ).doc_id,
                )
                while exist is True:
                    exist = self.check_match_already_play(
                        all_matchs_of_a_tournament,
                        self.player_table.get(
                            Play.ranking == list_of_players_by_score[j]["ranking"]
                        ).doc_id,
                        self.player_table.get(
                            Play.ranking
                            == list_of_players_by_score[j + 1 + k]["ranking"]
                        ).doc_id,
                    )

                    (
                        list_of_players_by_score[j + 1],
                        list_of_players_by_score[j + 1 + k],
                    ) = (
                        list_of_players_by_score[j + 1 + k],
                        list_of_players_by_score[j + 1],
                    )
                    k += 1

                new_match = Match.create_match(
                    self.player_table.get(
                        Play.ranking == list_of_players_by_score[j]["ranking"]
                    ).doc_id,
                    self.player_table.get(
                        Play.ranking == list_of_players_by_score[j + 1]["ranking"]
                    ).doc_id,
                )
                serialized_match = vars(new_match)
                self.match_table.insert(serialized_match)
                new_matchs_id.append(self.match_table.all()[-1].doc_id)
                j += 2
            list_of_rounds = self.tournament_table.all()[-1]["rounds"]
            list_of_rounds.append(self.round_table.all()[-1].doc_id)
            self.round_table.update(
                {"list_of_match": new_matchs_id},
                doc_ids=[self.round_table.all()[-1].doc_id],
            )

            self.tournament_table.update(
                {"rounds": list_of_rounds},
                doc_ids=[self.tournament_table.all()[-1].doc_id],
            )
            self.warning.round_create(str(self.round_table.all()[-1]["current_round"]))
            self.table.matchs()

    def choice_player_for_add_player_to_a_tournament(self):
        choice_player = self.select.add_player()
        return choice_player

    def check_match_already_play(self, list_match, id1, id2):
        exist = False
        for match in list_match:
            if collections.Counter([id1, id2]) == collections.Counter(match):
                exist = True
        return exist

    def create_end_tournament(self):
        self.warning.tournament_winner()
        self.tournament_table.update(
            {
                "end_date": json.dumps(
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S"), default=str
                )
            },
            doc_ids=[self.tournament_table.all()[-1].doc_id],
        )
        self.tournament_table.update(
            {"status_tournament": "finished"},
            doc_ids=[self.tournament_table.all()[-1].doc_id],
        )
        self.select.main_menu()
