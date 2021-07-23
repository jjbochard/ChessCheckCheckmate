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
        Run the code by displaying welcome message and maim menu
        """
        self.warning.welcome_message()
        self.main_menu()

    def main_menu(self):
        """
        Display main menu
        """
        while True:
            response = self.select.main_menu()
            if input_validators.is_valid_main_menu_response(response):
                break
        if response == "1":
            return self.manage_tournament()
        if response == "2":
            return self.create_player_main_menu()
        if response == "3":
            return self.change_ranking_menu()
        if response == "4":
            return self.tournaments_menu()
        if response == "5":
            return self.players_menu()
        if response == "6":
            return self.quit()

    def tournaments_menu(self):
        """
        Display tournaments menu
        """
        response = self.table.tournaments()
        while True:
            response = self.select.tournament_menu()
            if input_validators.is_valid_tournament_menu_response(response):
                break
        if response == "1":
            return self.choice_tournament_for_print_players()
        if response == "2":
            return self.choice_tournament_for_print_rounds()
        if response == "3":
            return self.choice_tournament_for_print_matchs()
        if response == "4":
            return self.change_ranking_menu()
        if response == "5":
            return self.main_menu()
        if response == "6":
            return self.quit()

    def choice_tournament_for_print_players(self):
        """
        Display a menu to choice wich manner to display players for a tournament
        Choices : ranking or alphabetical order
        """
        if not self.tournament_table:
            self.warning.no_tournament()
        else:
            while True:
                choice_tournament = self.select.choose_tournament_for_print_players()
                if input_validators.is_valid_id_tournament(choice_tournament):
                    break
            while True:
                choice_manner = self.select.print_players_menu()
                if input_validators.is_valid_print_players_menu_response(choice_manner):
                    break
            if choice_manner == "1":
                self.table.players_by_ranking_of_tournament(choice_tournament)
            else:
                self.table.players_by_alphabetical_order_of_tournament(
                    choice_tournament
                )
        self.tournaments_menu()

    def choice_tournament_for_print_rounds(self):
        """
        Display a menu to choice wich tournament to display rounds
        """
        if not self.tournament_table:
            self.warning.no_tournament()
        else:
            while True:
                choice_tournament = self.select.choose_tournament_for_print_rounds()
                if input_validators.is_valid_id_tournament(choice_tournament):
                    break
            self.table.rounds_of_tournament(choice_tournament)
        self.tournaments_menu()

    def choice_tournament_for_print_matchs(self):
        """
        Display a menu to choice wich tournament to display matchs
        """
        if not self.tournament_table:
            self.warning.no_tournament()
        else:
            while True:
                choice_tournament = self.select.choose_tournament_for_print_matchs()
                if input_validators.is_valid_id_tournament(choice_tournament):
                    break
            self.table.matchs_of_tournament(choice_tournament)
        self.tournaments_menu()

    def players_menu(self):
        """
        Display players menu
        """
        while True:
            response = self.select.players_menu()
            if input_validators.is_valid_players_menu_response(response):
                break
        if response == "1":
            return self.players_by_ranking()
        if response == "2":
            return self.players_by_alphabetical_order()
        if response == "3":
            return self.change_ranking_menu()
        if response == "4":
            return self.main_menu()
        if response == "5":
            return self.quit()

    def update_scores(self, match):
        """
        Update score of both Match and Player table
        Args:
            match: match to update
        """
        while True:
            response = self.select.write_score_menu(match)
            if input_validators.is_valid_write_score_menu_response(response):
                break
        Match.update_score_match(self, match, response, self.match_table)
        Player.update_score_player(self, match, response, self.player_table)

    def players_by_ranking(self):
        """
        Display players by ranking table
        """
        response = self.table.players_by_ranking()
        while True:
            response = self.select.players_by_ranking_menu()
            if input_validators.is_valid_players_by_ranking_menu_response(response):
                break
        if response == "1":
            return self.players_by_alphabetical_order()
        if response == "2":
            return self.change_ranking_menu()
        if response == "3":
            return self.main_menu()
        if response == "4":
            return self.quit()

    def players_by_alphabetical_order(self):
        """
        Display players by alphabetical order table
        """
        response = self.table.players_by_alphabetical_order()
        while True:
            response = self.select.players_by_alphabetical_order_menu()
            if input_validators.is_valid_players_by_alphabetical_order_menu_response(
                response
            ):
                break
        if response == "1":
            return self.players_by_ranking()
        if response == "2":
            return self.change_ranking_menu()
        if response == "3":
            return self.main_menu()
        if response == "4":
            return self.quit()

    def change_ranking_menu(self):
        """
        Display change ranking menu
        """
        if not self.player_table:
            self.warning.no_player()
            self.main_menu()
        else:
            self.table.players_by_id()
            while True:
                response = self.select.ranking_menu()
                if input_validators.is_valid_ranking_menu_response(response):
                    break
            if response == "1":
                return self.change_ranking()
            if response == "2":
                return self.main_menu()

    def choice_create_next_round(self):
        """
        Display a menu to let the user choice if he wants to create next round
        """
        while True:
            response = self.select.next_round_menu()
            if input_validators.is_valid_next_round_menu_response(response):
                break
        if response == "1":
            if self.is_new_tournament():
                return self.create_first_round()
            else:
                return self.create_round()
        if response == "2":
            return self.change_ranking()
        if response == "3":
            return self.main_menu()

    def choice_end_round(self):
        """
        Display a menu to let the user choice if he wants to end current round
        """
        while True:
            response = self.select.end_round_menu()
            if input_validators.is_valid_end_round_menu_response(response):
                break
        if response == "1":
            return self.end_round()
        if response == "2":
            return self.main_menu()

    def manage_tournament(self):
        """
        Allow to create tournament if not already exist and first and other rounds
        """
        if (
            Tournament.tournament_table_is_empty(self.tournament_table) is True
            or Tournament.status_tournament_is_finished(self.tournament_table) is True
        ):
            new_tournament = Tournament.create_tournament()
            serialized_tournament = vars(new_tournament)
            self.tournament_table.insert(serialized_tournament)
            self.add_players_to_tournament()
            self.choice_create_next_round()

        elif (
            Tournament.tournament_table_is_empty(self.tournament_table) is not True
            and self.round_table.all() == []
        ) or self.round_table.all()[-1]["status_round"] == "finished":
            self.choice_create_next_round()
        else:
            self.choice_end_round()

    def add_players_to_tournament(self):
        """
        Add players to tournament. Initialize their score to 0.
        """
        number_of_player = 0
        list_of_players_added = []
        list_of_remaining_players = Player.list_of_remaining_players(
            self, self.player_table
        )
        while number_of_player < 8:
            self.table.remaining_players(list_of_remaining_players)
            self.warning.remaining_players_to_add(number_of_player)
            while True:
                response = self.select.add_player_create_tournament_menu()
                if input_validators.is_valid_add_player_create_tournament_menu_response(
                    response
                ):
                    break
            if response == "1":
                if not self.player_table or list_of_remaining_players == []:
                    self.warning.no_player()
                    continue
                while True:
                    existed_player_id = int(
                        self.choice_player_for_add_player_to_a_tournament()
                    )
                    if input_validators.is_valid_id_player(existed_player_id) is True:
                        break
                list_of_players_added.append(existed_player_id)
            elif response == "2":
                new_player_id = self.create_player_in_tournament()
                existed_player_id = new_player_id
                list_of_players_added.append(new_player_id)
            number_of_player += 1
            contains_duplicates = any(
                list_of_players_added.count(element) > 1
                for element in list_of_players_added
            )
            if contains_duplicates:
                list_of_players_added.pop(-1)
                number_of_player -= 1
                self.warning.add_a_player_several_time()
                continue
            self.tournament_table.update(
                {"players": list_of_players_added},
                doc_ids=[self.tournament_table.all()[-1].doc_id],
            )
            Player.initialize_score(self, self.player_table, self.tournament_table)
            for player in list_of_remaining_players:
                if player[0] == existed_player_id:
                    list_of_remaining_players.remove(player)

    def create_player_main_menu(self):
        """
        Create player
        """
        new_player = Player.create_player()
        serialized_player = vars(new_player)
        self.player_table.insert(serialized_player)
        return self.main_menu()

    def create_player_in_tournament(self):
        """
        Create player
        Returns:
            new_player_id (int): id of the new player
        """
        new_player = Player.create_player()
        serialized_player = vars(new_player)
        self.player_table.insert(serialized_player)
        new_player_id = self.player_table.all()[-1].doc_id
        return new_player_id

    def get_input_new_ranking(self):
        """
        Get the input of the user when change ranking of a player
        Returns:
            new_ranking (int): new_ranking choice by the user
        """
        while True:
            id_player = int(self.select.change_ranking())
            if input_validators.is_valid_id_player(id_player):
                break
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
        """
        Check if the new ranking selected for a new player is already choosen
        Returns:
            Contains_duplicates (bool): depend on if the new ranking is already choosen
        """
        players_ranking = [player["ranking"] for player in self.player_table]
        return any(players_ranking.count(element) > 1 for element in players_ranking)

    def change_ranking(self):
        """
        Change ranking of a player
        """
        new_ranking = self.get_input_new_ranking()
        contains_duplicates = self.check_same_ranking()
        while contains_duplicates is True:
            self.table.players_by_id()
            self.warning.players_same_ranking(new_ranking)
            new_ranking = self.get_input_new_ranking()
            contains_duplicates = self.check_same_ranking()
        self.change_ranking_menu()

    def is_new_tournament(self):
        """
        Check if a tournament is a new one
        """
        if (
            self.round_table.all() == []
            or self.round_table.all()[-1]["current_round"] == 4
        ):
            return True

    def list_of_players_by_ranking(self):
        """
        Create a list of players sorted by ranking
        Returns:
            list_of_players_by_ranking (list): list of all the players of a tournament
        """
        list_ranking_player = [
            self.player_table.get(doc_id=player)
            for player in self.tournament_table.all()[-1]["players"]
        ]
        return Player.sort_list_of_players_by_ranking(self, list_ranking_player)

    def list_of_players_by_score(self):
        """
        Create a list of players sorted by score
        Returns:
            list_of_players_by_score (list): list of all the players of a tournament
        """
        list_score_player = [
            self.player_table.get(doc_id=player)
            for player in self.tournament_table.all()[-1]["players"]
        ]
        return Player.sort_list_of_players_by_score(self, list_score_player)

    def list_of_all_matchs_of_a_tournament(self):
        """
        Create a list of all matchs of a tournament
        Returns:
            all_matchs (list): list of all matchs of a tournament
        """
        all_matchs = []
        for rounds in self.tournament_table.all()[-1]["rounds"]:
            for matchs in self.round_table.all()[rounds - 1]["list_of_match"]:
                all_matchs.append(
                    [
                        self.match_table.all()[matchs - 1]["player_1"],
                        self.match_table.all()[matchs - 1]["player_2"],
                    ]
                )
        return all_matchs

    def end_round(self):
        """
        End a round by updating scores, and status_round and end sate of round table
        """
        for j in range(-4, 0):
            self.update_scores(self.match_table.all()[j])
        self.table.players_by_score()

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
        if self.round_table.all()[-1]["current_round"] == 4:
            self.end_tournament()
        else:
            return self.manage_tournament()

    def create_first_round(self):
        new_round = Round.create_round()
        serialized_round = vars(new_round)
        new_matchs_id = []
        self.round_table.insert(serialized_round)
        list_of_players_by_ranking = self.list_of_players_by_ranking()
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

        return self.manage_tournament()

    def create_round(self):
        """
        Create a round. Update tournament and round table
        """
        new_round = Round.create_round()
        serialized_round = vars(new_round)
        new_matchs_id = []
        serialized_round["current_round"] = (
            self.round_table.all()[-1]["current_round"] + 1
        )
        serialized_round["name"] = "Round " + str(serialized_round["current_round"])
        self.round_table.insert(serialized_round)
        list_of_players_by_score = self.list_of_players_by_score()
        all_matchs_of_a_tournament = self.list_of_all_matchs_of_a_tournament()
        Play = Query()
        j = 0
        for _ in range(4):
            k = 1
            while self.is_match_already_play(
                all_matchs_of_a_tournament,
                self.player_table.get(
                    Play.ranking == list_of_players_by_score[j]["ranking"]
                ).doc_id,
                self.player_table.get(
                    Play.ranking == list_of_players_by_score[j + 1]["ranking"]
                ).doc_id,
            ):
                self.is_match_already_play(
                    all_matchs_of_a_tournament,
                    self.player_table.get(
                        Play.ranking == list_of_players_by_score[j]["ranking"]
                    ).doc_id,
                    self.player_table.get(
                        Play.ranking == list_of_players_by_score[j + 1 + k]["ranking"]
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
        return self.manage_tournament()

    def choice_player_for_add_player_to_a_tournament(self):
        """
        Choice a player in the list of all the players in the database
        Returns:
            choice_player (int): id a the player choosen
        """
        return self.select.add_player()

    def is_match_already_play(self, list_match, id1, id2):
        """
        Check if a match has already been played
        Args:
            list_match (list): lists of couple of player's id
            id1: id of the player one
            id2: id of the player two
        """
        for match in list_match:
            if collections.Counter([id1, id2]) == collections.Counter(match):
                return True

    def end_tournament(self):
        """
        End a tournament by updating status and end date of tournament table and displaying winner
        """
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
        self.quit()

    def quit(self):
        """
        Close the program
        """
        self.warning.quit()
        return True
