import collections
import json
import random
from datetime import datetime

from tinydb import Query, TinyDB

import input_validators
from model import Match, Player, Round, Tournament


class Controller:
    def __init__(self, view):
        """ """
        self.view = view

    def run(self):
        """
        Loop that runs all the next
        'menu' methods from the controllers
        """
        self.view.welcome_message()
        self.methode_to_execute = self.welcome_menu
        while self.methode_to_execute is not None:
            next_method = self.methode_to_execute()
            self.methode_to_execute = next_method

    def welcome_menu(self):
        """ """

        while True:
            response = self.view.welcome_menu()
            if input_validators.is_valid_welcome_menu_response(response):
                break
        if response == "1":
            return self.create_tournament
        elif response == "2":
            return self.create_player
        elif response == "3":
            return self.display_change_ranking_menu
        elif response == "4":
            return self.display_tournaments_menu
        elif response == "5":
            return self.display_players_menu
        elif response == "6":
            return self.quit
        elif response == "7":
            return self.create_other_round

    def display_tournaments_menu(self):
        """ """
        response = self.view.display_tournaments()
        while True:
            response = self.view.display_tournaments_menu()
            if input_validators.is_valid_display_tournaments_menu_response(response):
                break

        if response == "1":
            return self.display_choice_tournament_for_print_players
        elif response == "2":
            return self.display_choice_tournament_for_print_rounds
        elif response == "3":
            return self.display_choice_tournament_for_print_matchs
        elif response == "4":
            return self.display_change_ranking_menu
        elif response == "5":
            return self.welcome_menu
        elif response == "6":
            return self.quit

    def display_choice_tournament_for_print_players(self):
        """ """
        choice_tournament = self.view.display_choice_tournament_for_print_players()
        response = self.view.display_players_for_a_tournament(choice_tournament)
        while True:
            response = self.view.display_tournaments_menu()
            if input_validators.is_valid_display_tournaments_menu_response(response):
                break

        if response == "1":
            return self.display_choice_tournament_for_print_players
        elif response == "2":
            return self.display_choice_tournament_for_print_rounds
        elif response == "3":
            return self.display_choice_tournament_for_print_matchs
        elif response == "4":
            return self.display_change_ranking_menu
        elif response == "5":
            return self.welcome_menu
        elif response == "6":
            return self.quit

    def display_choice_tournament_for_print_rounds(self):
        """ """
        choice_tournament = self.view.display_choice_tournament_for_print_rounds()
        response = self.view.display_rounds_for_a_tournament(choice_tournament)
        while True:
            response = self.view.display_tournaments_menu()
            if input_validators.is_valid_display_tournaments_menu_response(response):
                break

        if response == "1":
            return self.display_choice_tournament_for_print_players
        elif response == "2":
            return self.display_choice_tournament_for_print_rounds
        elif response == "3":
            return self.display_choice_tournament_for_print_matchs
        elif response == "4":
            return self.display_change_ranking_menu
        elif response == "5":
            return self.welcome_menu
        elif response == "6":
            return self.quit

    def display_choice_tournament_for_print_matchs(self):
        """ """
        choice_tournament = self.view.display_choice_tournament_for_print_matchs()
        response = self.view.display_matchs_for_a_tournament(choice_tournament)
        while True:
            response = self.view.display_tournaments_menu()
            if input_validators.is_valid_display_tournaments_menu_response(response):
                break

        if response == "1":
            return self.display_choice_tournament_for_print_players
        elif response == "2":
            return self.display_choice_tournament_for_print_rounds
        elif response == "3":
            return self.display_choice_tournament_for_print_matchs
        elif response == "4":
            return self.display_change_ranking_menu
        elif response == "5":
            return self.welcome_menu
        elif response == "6":
            return self.quit

    def display_players_menu(self):
        """ """
        while True:
            response = self.view.display_players_menu()
            if input_validators.is_valid_display_players_menu_response(response):
                break

        if response == "1":
            return self.display_players_by_ranking
        elif response == "2":
            return self.display_players_by_alphabetical_order
        elif response == "3":
            return self.display_change_ranking_menu
        elif response == "4":
            return self.welcome_menu
        elif response == "5":
            return self.quit

    def display_players_by_ranking(self):
        """ """
        response = self.view.display_players_by_ranking()
        while True:
            response = self.view.display_players_by_ranking_menu()
            if input_validators.is_valid_display_players_by_ranking_menu_response(
                response
            ):
                break

        if response == "1":
            return self.display_players_by_alphabetical_order
        elif response == "2":
            return self.display_change_ranking_menu
        elif response == "3":
            return self.welcome_menu
        elif response == "4":
            return self.quit

    def display_players_by_alphabetical_order(self):
        """ """
        response = self.view.display_players_by_alphabetical_order()
        while True:
            response = self.view.display_players_by_alphabetical_order_menu()
            if input_validators.is_valid_display_players_by_alphabetical_order_menu_response(
                response
            ):
                break

        if response == "1":
            return self.display_players_by_ranking
        elif response == "2":
            return self.display_change_ranking_menu
        elif response == "3":
            return self.welcome_menu
        elif response == "4":
            return self.quit

    def display_change_ranking_menu(self):
        self.view.display_players_by_alphabetical_order()
        while True:
            response = self.view.display_ranking_menu()
            if input_validators.is_valid_display_change_ranking_menu_response(response):
                break
        if response == "1":
            return self.change_ranking
        elif response == "2":
            return self.welcome_menu

    def quit(self):
        """
        Close the program
        """
        self.view.quit()

    def create_tournament(self):
        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        new_tournament = Tournament.create_tournament()
        serialized_tournament = vars(new_tournament)
        tournament_table.insert(serialized_tournament)
        self.add_players_to_tournament()
        # while round_table.all()[-1]["current_round"] < 4:
        for i in range(4):
            self.create_round()
            i += 1

    def add_players_to_tournament(self):
        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        player_table = db.table("player")
        # number_of_player = 0
        list_of_players = [1, 2, 3, 4, 5, 6, 7, 8]
        # while number_of_player < 8:
        #     self.view.display_remaining_players_to_add(number_of_player)
        #     self.view.display_players_by_id()
        #     while True:
        #         response = self.view.display_choice_add_players_create_tournament()
        #         if input_validators.is_valid_display_choice_add_players_create_tournament_menu_response(
        #             response
        #         ):
        #             break
        #     if response == "1":
        #         existed_player_id = int(
        #             self.choice_player_for_add_player_to_a_tournament()
        #         )
        #         list_of_players.append(existed_player_id)
        #     elif response == "2":
        #         new_player_id = self.create_player()
        #         list_of_players.append(new_player_id)

        #     self.view.display_player_already_choosen(list_of_players)
        #     number_of_player += 1

        #     contains_duplicates = any(
        #         list_of_players.count(element) > 1 for element in list_of_players
        #     )
        #     if contains_duplicates is True:
        #         list_of_players.pop(-1)
        #         number_of_player -= 1
        #         self.view.display_warning_add_a_player_several_time()
        #         continue

        #     tournament_table.update(
        #         {"players": list_of_players},
        #         doc_ids=[tournament_table.all()[-1].doc_id],
        #     )
        #     for player in tournament_table.all()[-1]["players"]:
        #         player_table.update(
        #             {"score": 0},
        #             doc_ids=[player_table.all()[player - 1].doc_id],
        #         )
        tournament_table.update(
            {"players": list_of_players},
            doc_ids=[tournament_table.all()[-1].doc_id],
        )
        for player in tournament_table.all()[-1]["players"]:
            player_table.update(
                {"score": 0},
                doc_ids=[player_table.all()[player - 1].doc_id],
            )

    def create_player(self):
        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        player_table = db.table("player")
        new_player = Player.create_player()
        serialized_player = vars(new_player)
        player_table.insert(serialized_player)
        new_player_id = player_table.all()[-1].doc_id
        if (
            tournament_table.all()[-1]["state_tournament"] == "finished"
            or not tournament_table.all()
        ):
            return self.welcome_menu
        else:
            return new_player_id

    def get_input_new_ranking(self):
        db = TinyDB("db.json")
        player_table = db.table("player")
        id_player = int(self.view.choice_player_to_change_ranking())
        new_ranking = int(
            input(
                "Enter a new ranking for "
                + str(
                    player_table.all()[id_player - 1]["first_name"]
                    + " "
                    + str(player_table.all()[id_player - 1]["last_name"] + "\n")
                )
            )
        )
        player_table.update(
            {"ranking": new_ranking},
            doc_ids=[player_table.all()[id_player - 1].doc_id],
        )
        return new_ranking

    def check_same_ranking(self):
        db = TinyDB("db.json")
        player_table = db.table("player")
        players_ranking = []
        for player in player_table:
            players_ranking.append(player["ranking"])
        contains_duplicates = any(
            players_ranking.count(element) > 1 for element in players_ranking
        )
        return contains_duplicates

    def change_ranking(self):
        new_ranking = self.get_input_new_ranking()
        contains_duplicates = self.check_same_ranking()
        while contains_duplicates is True:
            self.view.display_warning_players_same_ranking(new_ranking)
            new_ranking = self.get_input_new_ranking()
            contains_duplicates = self.check_same_ranking()
        return self.display_change_ranking_menu

    def create_round(self):
        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        player_table = db.table("player")
        round_table = db.table("round")
        match_table = db.table("match")
        new_round = Round.create_round()
        serialized_round = vars(new_round)
        if round_table.all()[-1]["current_round"] == 4 or not round_table.all():
            round_table.insert(serialized_round)
            list_ranking_player = []
            new_matchs_id = []
            for player in tournament_table.all()[-1]["players"]:
                list_ranking_player.append((player_table.get(doc_id=player)))
            list_of_players_by_ranking = Player.make_list_of_players_by_ranking(
                self, list_ranking_player
            )
            Play = Query()
            for i in range(4):
                new_match = self.generate_color_player(
                    player_table.get(
                        Play.ranking == list_of_players_by_ranking[0][i]["ranking"]
                    ).doc_id,
                    player_table.get(
                        Play.ranking == list_of_players_by_ranking[1][i]["ranking"]
                    ).doc_id,
                )
                serialized_match = vars(new_match)
                match_table.insert(serialized_match)
                new_matchs_id.append(match_table.all()[-1].doc_id)
            list_of_rounds = tournament_table.all()[-1]["rounds"]
            list_of_rounds.append(round_table.all()[-1].doc_id)
            round_table.update(
                {"list_of_match": new_matchs_id},
                doc_ids=[round_table.all()[-1].doc_id],
            )
            tournament_table.update(
                {"rounds": list_of_rounds},
                doc_ids=[tournament_table.all()[-1].doc_id],
            )
            self.view.display_message_first_round_create()
            self.view.display_match_information()
            self.write_score()

        else:
            serialized_round["current_round"] = (
                round_table.all()[-1]["current_round"] + 1
            )
            serialized_round["name"] = "Round " + str(serialized_round["current_round"])

            round_table.insert(serialized_round)

            list_score_player = []
            new_matchs_id = []
            for player in tournament_table.all()[-1]["players"]:
                list_score_player.append((player_table.get(doc_id=player)))
            list_of_players_by_score = Player.make_list_of_players_by_score(
                self, list_score_player
            )
            all_matchs_of_a_tournament = []
            for rounds in tournament_table.all()[-1]["rounds"]:
                for matchs in round_table.all()[rounds - 1]["list_of_match"]:
                    all_matchs_of_a_tournament.append(
                        [
                            match_table.all()[matchs - 1]["match"][0][0],
                            match_table.all()[matchs - 1]["match"][1][0],
                        ]
                    )
            Play = Query()
            j = 0
            for i in range(4):
                k = 1
                exist = self.check_match_already_play(
                    all_matchs_of_a_tournament,
                    player_table.get(
                        Play.ranking == list_of_players_by_score[j]["ranking"]
                    ).doc_id,
                    player_table.get(
                        Play.ranking == list_of_players_by_score[j + 1]["ranking"]
                    ).doc_id,
                )
                while exist is True:
                    exist = self.check_match_already_play(
                        all_matchs_of_a_tournament,
                        player_table.get(
                            Play.ranking == list_of_players_by_score[j]["ranking"]
                        ).doc_id,
                        player_table.get(
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

                new_match = self.generate_color_player(
                    player_table.get(
                        Play.ranking == list_of_players_by_score[j]["ranking"]
                    ).doc_id,
                    player_table.get(
                        Play.ranking == list_of_players_by_score[j + 1]["ranking"]
                    ).doc_id,
                )
                serialized_match = vars(new_match)
                match_table.insert(serialized_match)
                new_matchs_id.append(match_table.all()[-1].doc_id)
                j += 2
            list_of_rounds = tournament_table.all()[-1]["rounds"]
            list_of_rounds.append(round_table.all()[-1].doc_id)
            round_table.update(
                {"list_of_match": new_matchs_id},
                doc_ids=[round_table.all()[-1].doc_id],
            )

            tournament_table.update(
                {"rounds": list_of_rounds},
                doc_ids=[tournament_table.all()[-1].doc_id],
            )
            self.view.display_message_other_round_create(
                str(round_table.all()[-1]["current_round"])
            )
            self.view.display_match_information()
            self.write_score()
            if round_table.all()[-1]["current_round"] == 4:
                self.create_end_tournament()

    def choice_player_for_add_player_to_a_tournament(self):
        choice_player = self.view.display_choice_player_to_append_to_a_tournament()
        return choice_player

    def write_score(self):
        db = TinyDB("db.json")
        match_table = db.table("match")
        round_table = db.table("round")
        player_table = db.table("player")

        i = -4
        j = -4
        index = 0
        matchs_to_write_score = []
        while len(matchs_to_write_score) < 4:
            matchs_to_write_score.append(match_table.all()[j])
            j += 1
        for match in matchs_to_write_score:
            update_match = matchs_to_write_score[index]
            update_match["match"][0][1] = player_table.all()[
                update_match["match"][0][0] - 1
            ]["score"] + float(
                input(
                    "Enter the score of the player number "
                    + str(update_match["match"][0][0])
                    + ":\n "
                )
            )
            update_match["match"][1][1] = player_table.all()[
                update_match["match"][1][0] - 1
            ]["score"] + float(
                input(
                    "Enter the score of the player number "
                    + str(update_match["match"][1][0])
                    + ":\n "
                )
            )
            match_table.update(
                {"match": update_match["match"]},
                doc_ids=[match_table.all()[i].doc_id],
            )
            player_table.update(
                {"score": update_match["match"][0][1]},
                doc_ids=[
                    (player_table.all()[(update_match["match"][0][0]) - 1]).doc_id
                ],
            )
            player_table.update(
                {"score": update_match["match"][1][1]},
                doc_ids=[
                    (player_table.all()[(update_match["match"][1][0]) - 1]).doc_id
                ],
            )
            i += 1
            index += 1
        round_table.update(
            {
                "end_date": json.dumps(
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S"), default=str
                )
            },
            doc_ids=[round_table.all()[-1].doc_id],
        )
        self.view.display_players_by_score()

    def generate_color_player(self, player_1, player_2):
        black_or_white = random.randrange(2)
        if black_or_white == 0:
            new_match = Match(player_1, player_2)
        else:
            new_match = Match(player_2, player_1)
        return new_match

    def check_match_already_play(self, list_match, id1, id2):
        exist = False
        for match in list_match:
            if collections.Counter([id1, id2]) == collections.Counter(match):
                exist = True
        return exist

    def create_end_tournament(self):
        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        tournament_table.update(
            {
                "end_date": json.dumps(
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S"), default=str
                )
            },
            doc_ids=[tournament_table.all()[-1].doc_id],
        )
        tournament_table.update(
            {"state_tournament": "finished"},
            doc_ids=[tournament_table.all()[-1].doc_id],
        )
