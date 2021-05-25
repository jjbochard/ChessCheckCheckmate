import collections
import json
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
        elif response == "5":
            return self.display_tournaments_menu
        elif response == "6":
            return self.display_players_menu
        elif response == "8":
            return self.quit
        elif response == "9":
            return self.display_players_menu

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
            return self.welcome_menu
        elif response == "5":
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
            return self.welcome_menu
        elif response == "5":
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
            return self.welcome_menu
        elif response == "5":
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
            return self.welcome_menu
        elif response == "5":
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
            return self.welcome_menu
        elif response == "4":
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
            return self.welcome_menu
        elif response == "3":
            return self.quit

        response = self.view.display_players_menu()

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
            return self.welcome_menu
        elif response == "3":
            return self.quit

        response = self.view.display_players_menu()

    def quit(self):
        """
        Close the program
        """
        self.view.quit()

    def create_tournament(self):
        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        round_table = db.table("round")
        new_tournament = Tournament.create_tournament()
        serialized_tournament = vars(new_tournament)
        tournament_table.insert(serialized_tournament)
        self.add_players_to_tournament()
        self.create_first_round()
        while round_table.all()[-1]["current_round"] < 4:
            self.create_other_round()

    def add_players_to_tournament(self):
        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        player_table = db.table("player")
        number_of_player = 0
        list_of_players = []
        while number_of_player < 8:
            self.view.display_remaining_players_to_add(number_of_player)
            self.view.display_players_by_id()
            while True:
                response = self.view.display_choice_add_players_create_tournament()
                if input_validators.is_valid_display_choice_add_players_create_tournament_menu_response(
                    response
                ):
                    break
            if response == "1":
                existed_player_id = int(
                    self.choice_player_for_add_player_to_a_tournament()
                )
                list_of_players.append(existed_player_id)
            elif response == "2":
                new_player_id = self.create_player()
                list_of_players.append(new_player_id)

            self.view.display_player_already_choosen(list_of_players)
            number_of_player += 1

            contains_duplicates = any(
                list_of_players.count(element) > 1 for element in list_of_players
            )
            if contains_duplicates is True:
                list_of_players.pop(-1)
                number_of_player -= 1
                self.view.display_warning_add_a_player_several_time()
                continue

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
        player_table = db.table("player")
        new_player = Player.create_player()
        serialized_player = vars(new_player)
        player_table.insert(serialized_player)
        new_player_id = player_table.all()[-1].doc_id
        return new_player_id

    def create_round(self):
        db = TinyDB("db.json")
        round_table = db.table("round")
        new_round = Round.create_round()
        serialized_round = vars(new_round)
        round_table.insert(serialized_round)
        new_round_id = round_table.all()[-1].doc_id
        return new_round_id

    def choice_player_for_add_player_to_a_tournament(self):
        choice_player = self.view.display_choice_player_to_append_to_a_tournament()
        return choice_player

    def create_first_round(self):
        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        player_table = db.table("player")
        match_table = db.table("match")
        round_table = db.table("round")
        list_ranking_player = []
        new_matchs_id = []
        new_rounds_id = []
        for player in tournament_table.all()[-1]["players"]:
            list_ranking_player.append((player_table.get(doc_id=player)))
        list_of_players_by_ranking = Player.make_list_of_players_by_ranking(
            self, list_ranking_player
        )
        Play = Query()
        for i in range(
            int(
                (
                    len(
                        tournament_table.get(doc_id=tournament_table.all()[-1].doc_id)[
                            "players"
                        ]
                    )
                )
                / 2
            )
        ):
            new_match = Match(
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
        new_round_id = self.create_round()
        new_rounds_id.append(new_round_id)

        round_table.update(
            {"list_of_match": new_matchs_id},
            doc_ids=[round_table.all()[-1].doc_id],
        )
        tournament_table.update(
            {"rounds": new_rounds_id},
            doc_ids=[tournament_table.all()[-1].doc_id],
        )
        self.view.display_message_first_round_create()
        self.write_score()

    def create_other_round(self):
        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        player_table = db.table("player")
        match_table = db.table("match")
        round_table = db.table("round")
        list_score_player = []
        new_matchs_id = []
        for player in tournament_table.all()[-1]["players"]:
            list_score_player.append((player_table.get(doc_id=player)))
        list_of_players_by_score = Player.make_list_of_players_by_score(
            self, list_score_player
        )
        all_matchs = []
        for rounds in tournament_table.all()[-1]["rounds"]:
            for matchs in round_table.all()[rounds - 1]["list_of_match"]:
                all_matchs.append(
                    [
                        match_table.all()[matchs - 1]["match"][0][0],
                        match_table.all()[matchs - 1]["match"][1][0],
                    ]
                )
        Play = Query()
        print(all_matchs)
        for i in range(
            int(
                (
                    len(
                        tournament_table.get(doc_id=tournament_table.all()[-1].doc_id)[
                            "players"
                        ]
                    )
                )
                / 2
            )
        ):
            for match in all_matchs:
                if collections.Counter(match) == collections.Counter(
                    [
                        player_table.get(
                            Play.ranking == list_of_players_by_score[0][i]["ranking"]
                        ).doc_id,
                        player_table.get(
                            Play.ranking == list_of_players_by_score[1][i]["ranking"]
                        ).doc_id,
                    ]
                ):
                    print("same opponent")
                    for player in list_of_players_by_score[1]:
                        print(player["ranking"])

                    (
                        list_of_players_by_score[1][i],
                        list_of_players_by_score[1][i + 1],
                    ) = (
                        list_of_players_by_score[1][i + 1],
                        list_of_players_by_score[1][i],
                    )
                    for player in list_of_players_by_score[1]:
                        print(player["ranking"])

                    new_match = Match(
                        player_table.get(
                            Play.ranking == list_of_players_by_score[0][i]["ranking"]
                        ).doc_id,
                        player_table.get(
                            Play.ranking == list_of_players_by_score[1][i]["ranking"]
                        ).doc_id,
                    )

                else:
                    new_match = Match(
                        player_table.get(
                            Play.ranking == list_of_players_by_score[0][i]["ranking"]
                        ).doc_id,
                        player_table.get(
                            Play.ranking == list_of_players_by_score[1][i]["ranking"]
                        ).doc_id,
                    )

            serialized_match = vars(new_match)
            match_table.insert(serialized_match)
            new_matchs_id.append(match_table.all()[-1].doc_id)
        new_round_id = self.create_round()
        round_table.update(
            {"list_of_match": new_matchs_id},
            doc_ids=[round_table.all()[-1].doc_id],
        )
        round_table.update(
            {"current_round": (round_table.all()[-2]["current_round"]) + 1},
            doc_ids=[round_table.all()[-1].doc_id],
        )
        round_table.update(
            {"name": "Round " + str(round_table.all()[-1]["current_round"])},
            doc_ids=[round_table.all()[-1].doc_id],
        )

        new_list_of_round = tournament_table.all()[-1]["rounds"]
        new_list_of_round.append(new_round_id)
        tournament_table.update(
            {"rounds": new_list_of_round},
            doc_ids=[tournament_table.all()[-1].doc_id],
        )
        self.view.display_message_other_round_create(
            str(round_table.all()[-1]["current_round"])
        )
        self.write_score()
        print(round_table.all()[-1]["current_round"])
        if round_table.all()[-1]["current_round"] == 4:
            self.create_end_date_tournament()

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

    def create_end_date_tournament(self):
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
