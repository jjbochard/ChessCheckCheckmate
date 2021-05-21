from tabulate import tabulate
from tinydb import TinyDB


class View:
    def welcome_message(self):
        """ """
        welcome_message = print(
            "\n" "====================\n" "\n" "Welcome to Ultimate Chess Manage" "\n"
        )

        return welcome_message

    def welcome_menu(self):
        """ """
        # print("")
        menu_choice = input(
            "=========="
            "\n"
            "\nWhat do you want to do :\n"
            "  1 - Start a tournament\n"
            # "  2 - Add a player\n"
            # "  3 - Show ranking\n"
            # "  4 - Change ranking\n"
            "  5 - Display tournaments\n"
            "  6 - Display players\n"
            # "  7 - Show ranking\n"
            "  8 - Quit\n"
            "  9 - Test\n"
        )

        return menu_choice

    def display_tournaments_menu(self):
        """ """
        # print("")
        menu_choice = input(
            "\nWhat do you want to do :\n"
            "  1 - Display players of a tournament\n"
            "  2 - Display rounds of a tournament\n"
            "  3 - Display matchs of a tournament\n"
            "  4 - Go to main menu\n"
            "  5 - Quit\n"
        )

        return menu_choice

    def display_choice_player_to_append_to_a_tournament(self):
        choice_player = input(
            "Which player do you want to add to this tournament : (choose an id)\n"
        )
        return choice_player

    def display_choice_tournament_for_print_players(self):
        choice_tournament = input(
            "For which tournament do you want to display players : (choose an id)\n"
        )
        return choice_tournament

    def display_players_for_a_tournament(self, choice_tournament):
        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        player_table = db.table("player")
        chooses_tournament = tournament_table.all()[int(choice_tournament) - 1]
        players_for_a_tournament = []
        for players in chooses_tournament["players"]:
            players_for_a_tournament.append(player_table.all()[players - 1])
        players_for_a_tournament_for_print = []
        for player in players_for_a_tournament:
            players_for_a_tournament_for_print.append(
                [
                    player["last_name"],
                    player["first_name"],
                    player["ranking"],
                    player["date_of_birth"],
                    player["gender"],
                ]
            )
        players_for_a_tournament_for_print = sorted(players_for_a_tournament_for_print)
        print(
            tabulate(
                players_for_a_tournament_for_print,
                headers=[
                    "First name",
                    "Last name",
                    "Ranking",
                    "Date of birth",
                    "Gender",
                ],
            )
        )

    def display_choice_tournament_for_print_rounds(self):
        choice_tournament = input(
            "For which tournament do you want to display rounds : (choose an id)\n"
        )
        return choice_tournament

    def display_rounds_for_a_tournament(self, choice_tournament):
        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        round_table = db.table("round")
        chooses_tournament = tournament_table.all()[int(choice_tournament) - 1]
        rounds_for_a_tournament = []
        for rounds in chooses_tournament["rounds"]:
            rounds_for_a_tournament.append(round_table.all()[rounds - 1])
        rounds_for_a_tournament_for_print = []
        for round in rounds_for_a_tournament:
            rounds_for_a_tournament_for_print.append(
                [
                    round["name"],
                    round["start_date"],
                    round["end_date"],
                    round["list_of_match"],
                ]
            )
        rounds_for_a_tournament_for_print = sorted(rounds_for_a_tournament_for_print)
        print(
            tabulate(
                rounds_for_a_tournament_for_print,
                headers=[
                    "Name",
                    "Start date",
                    "End date",
                    "List of match",
                ],
            )
        )

    def display_choice_tournament_for_print_matchs(self):
        choice_tournament = input(
            "For which tournament do you want to display matchs : (choose an id)\n"
        )
        return choice_tournament

    def display_matchs_for_a_tournament(self, choice_tournament):
        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        round_table = db.table("round")
        match_table = db.table("match")
        chooses_tournament = tournament_table.all()[int(choice_tournament) - 1]
        matchs_for_a_tournament = []
        for round in chooses_tournament["rounds"]:
            for match in round_table.all()[round - 1]["list_of_match"]:
                matchs_for_a_tournament.append(match_table.all()[match - 1])
        matchs_for_a_tournament_for_print = []
        for match in matchs_for_a_tournament:
            matchs_for_a_tournament_for_print.append(
                [match.doc_id, match["match"][0][0], match["match"][1][0]]
            )
        matchs_for_a_tournament_for_print = sorted(matchs_for_a_tournament_for_print)
        print(
            tabulate(
                matchs_for_a_tournament_for_print,
                headers=[
                    "Id",
                    "Player 1",
                    "Player 2",
                ],
            )
        )

    def display_players_menu(self):
        """ """
        # print("")
        menu_choice = input(
            "  1 - Display players by rank\n"
            "  2 - Display players by alphabetical order\n"
            "  3 - Go to main menu\n"
            "  4 - Quit\n"
        )

        return menu_choice

    def display_tournaments(self):
        """ """
        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        tournaments = []
        for tournament in tournament_table:
            tournaments.append(
                [
                    tournament.doc_id,
                    tournament["name"],
                    tournament["place"],
                    tournament["start_date"],
                    tournament["end_date"],
                    tournament["time_control"],
                    tournament["description"],
                ]
            )
        print(
            tabulate(
                tournaments,
                headers=[
                    "Id",
                    "Name",
                    "Place",
                    "Start date",
                    "End date",
                    "Time control",
                    "Description",
                ],
            )
        )

    def display_players_by_ranking(self):
        """ """
        db = TinyDB("db.json")
        player_table = db.table("player")
        players = []
        for player in player_table:
            players.append(
                [
                    player["ranking"],
                    player["last_name"],
                    player["first_name"],
                    player["date_of_birth"],
                    player["gender"],
                ]
            )
        players = sorted(players)
        print(
            tabulate(
                players,
                headers=[
                    "Ranking",
                    "First name",
                    "Last name",
                    "Date of birth",
                    "Gender",
                ],
            )
        )

    def display_players_by_ranking_menu(self):
        """ """
        # print("")
        menu_choice = input(
            "  1 - Display players by alphabetical order\n"
            "  2 - Go to main menu\n"
            "  3 - Quit\n"
        )
        return menu_choice

    def display_players_by_alphabetical_order(self):
        """ """
        db = TinyDB("db.json")
        player_table = db.table("player")
        players = []
        for player in player_table:
            players.append(
                [
                    player["last_name"],
                    player["first_name"],
                    player["ranking"],
                    player["date_of_birth"],
                    player["gender"],
                ]
            )
        players = sorted(players)
        print(
            tabulate(
                players,
                headers=[
                    "First name",
                    "Last name",
                    "Ranking",
                    "Date of birth",
                    "Gender",
                ],
            )
        )

    def display_players_by_id(self):
        """ """
        db = TinyDB("db.json")
        player_table = db.table("player")
        players = []
        for player in player_table:
            players.append(
                [
                    player.doc_id,
                    player["last_name"],
                    player["first_name"],
                    player["date_of_birth"],
                    player["gender"],
                ]
            )
        players = sorted(players)
        print(
            tabulate(
                players,
                headers=[
                    "Id",
                    "First name",
                    "Last name",
                    "Date of birth",
                    "Gender",
                ],
            )
        )

    def display_choice_add_players_create_tournament(self):
        menu_choice = input("\n  1 - Add existed players\n" "  2 - Add a new player\n")
        return menu_choice

    def display_players_by_alphabetical_order_menu(self):
        """ """
        menu_choice = input(
            "  1 - Display players by rank\n" "  2 - Go to main menu\n" "  3 - Quit\n"
        )
        return menu_choice

    def display_remaining_players_to_add(self, number_of_player):
        print("\n" + str(8 - number_of_player) + " players remaining\n")

    def display_player_already_choosen(self, list_of_players):
        print("Players already choosen :")
        print(*list_of_players)

    def display_warning_add_a_player_several_time(self):
        print("Player alredy choosen. Please add an other player\n")

    def display_message_first_round_create(self):
        print("First round has been created")

    def display_message_other_round_create(self, round_number):
        print("Round " + str(round_number) + " has been created")

    def quit(self):
        """
        Display a thank you message when the user qui the program
        """
        print("\nClosing the program...\n")
