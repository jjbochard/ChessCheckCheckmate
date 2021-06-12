from tabulate import tabulate
from tinydb import TinyDB


class View:
    def welcome_message(self):
        """ """
        welcome_message = print(
            "\n" "====================\n" "\n" "Welcome to Ultimate Chess Manager" "\n"
        )

        return welcome_message

    def welcome_menu(self):
        """ """
        menu_choice = input(
            "=========="
            "\n"
            "  1 - Start a tournament\n"
            "  2 - Create a player\n"
            "  3 - Change ranking\n"
            "  4 - Display tournaments\n"
            "  5 - Display players\n"
            "  6 - Quit\n"
        )

        return menu_choice

    def welcome_menu_continue(self):
        """ """
        menu_choice = input(
            "=========="
            "\n"
            "  1 - Continue a tournament\n"
            "  2 - Create a player\n"
            "  3 - Change ranking\n"
            "  4 - Display tournaments\n"
            "  5 - Display players\n"
            "  6 - Quit\n"
            "  7 - Test\n"
        )

        return menu_choice

    def display_tournaments_menu(self):
        """ """
        # print("")
        menu_choice = input(
            "  1 - Display players of a tournament\n"
            "  2 - Display rounds of a tournament\n"
            "  3 - Display matchs of a tournament\n"
            "  4 - Change ranking\n"
            "  5 - Go to main menu\n"
            "  6 - Quit\n"
        )

        return menu_choice

    def display_choice_create_next_round_menu(self):
        """ """
        menu_choice = input(
            "\n" "  1 - Create next round\n" "  2 - Go to main menu\n" "  3 - Quit\n"
        )
        return menu_choice

    def display_choice_end_round_menu(self):
        """ """
        menu_choice = input(
            "\n" "  1 - End round\n" "  2 - Go to main menu\n" "  3 - Quit\n"
        )
        return menu_choice

    def display_choice_player_to_append_to_a_tournament(self):
        choice_player = input(
            "Which player do you want to add to this tournament (choose an id): "
        )
        return choice_player

    def display_choice_tournament_for_print_players(self):
        choice_tournament = input(
            "For which tournament do you want to display players (choose an id): "
        )
        return choice_tournament

    def display_choice_manner_to_print_players_menu(self):
        choice_manner = input(
            "\n"
            "  1 - Display players by ranking\n"
            "  2 - Display players by alphabetical order\n"
        )
        return choice_manner

    def display_players_by_ranking_for_a_tournament(self, choice_tournament):
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
                    player["ranking"],
                    player["last_name"],
                    player["first_name"],
                    player["date_of_birth"],
                    player["gender"],
                ]
            )
        players_for_a_tournament_for_print = sorted(players_for_a_tournament_for_print)
        print(
            tabulate(
                players_for_a_tournament_for_print,
                headers=[
                    "Ranking",
                    "First name",
                    "Last name",
                    "Date of birth",
                    "Gender",
                ],
                tablefmt="fancy_grid",
            )
        )

    def display_players_by_alphabetical_order_for_a_tournament(self, choice_tournament):
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
        players_for_a_tournament_for_print = sorted(
            players_for_a_tournament_for_print, key=lambda k: (k[0], k[1])
        )
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
                tablefmt="fancy_grid",
            )
        )

    def display_choice_tournament_for_print_rounds(self):
        choice_tournament = input(
            "For which tournament do you want to display rounds (choose an id): "
        )
        return choice_tournament

    def display_rounds_for_a_tournament(self, choice_tournament):
        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        player_table = db.table("player")
        round_table = db.table("round")
        match_table = db.table("match")
        chooses_tournament = tournament_table.all()[int(choice_tournament) - 1]
        rounds_for_a_tournament = []
        matchs_for_a_tournament = []
        for round in chooses_tournament["rounds"]:
            rounds_for_a_tournament.append(round_table.all()[round - 1])
            for match in round_table.all()[round - 1]["list_of_match"]:
                matchs_for_a_tournament.append(match_table.all()[match - 1])

        rounds_for_a_tournament_for_print = []
        i = 0
        for round in rounds_for_a_tournament:
            rounds_for_a_tournament_for_print.append(
                [
                    round["name"],
                    round["start_date"],
                    round["end_date"],
                ]
            )
            matchs_of_round = []
            for match in round["list_of_match"]:
                if (
                    matchs_for_a_tournament[match - 1]["match"][0][1] == 1.0
                    and matchs_for_a_tournament[match - 1]["match"][1][1] == 0.0
                ):
                    matchs_of_round.append(
                        player_table.get(
                            doc_id=matchs_for_a_tournament[match - 1]["match"][0][0]
                        )["first_name"]
                        + " "
                        + player_table.get(
                            doc_id=matchs_for_a_tournament[match - 1]["match"][0][0]
                        )["last_name"]
                        + " won against "
                        + player_table.get(
                            doc_id=matchs_for_a_tournament[match - 1]["match"][1][0]
                        )["first_name"]
                        + " "
                        + player_table.get(
                            doc_id=matchs_for_a_tournament[match - 1]["match"][1][0]
                        )["last_name"]
                        + "\n",
                    )
                elif (
                    matchs_for_a_tournament[match - 1]["match"][0][1] == 0.0
                    and matchs_for_a_tournament[match - 1]["match"][1][1] == 1.0
                ):
                    matchs_of_round.append(
                        player_table.get(
                            doc_id=matchs_for_a_tournament[match - 1]["match"][1][0]
                        )["first_name"]
                        + " "
                        + player_table.get(
                            doc_id=matchs_for_a_tournament[match - 1]["match"][1][0]
                        )["last_name"]
                        + " won against "
                        + player_table.get(
                            doc_id=matchs_for_a_tournament[match - 1]["match"][0][0]
                        )["first_name"]
                        + " "
                        + player_table.get(
                            doc_id=matchs_for_a_tournament[match - 1]["match"][0][0]
                        )["last_name"]
                        + "\n",
                    )
                elif (
                    matchs_for_a_tournament[match - 1]["match"][0][1] == 0.5
                    and matchs_for_a_tournament[match - 1]["match"][1][1] == 0.5
                ):
                    matchs_of_round.append(
                        player_table.get(
                            doc_id=matchs_for_a_tournament[match - 1]["match"][1][0]
                        )["first_name"]
                        + " "
                        + player_table.get(
                            doc_id=matchs_for_a_tournament[match - 1]["match"][1][0]
                        )["last_name"]
                        + " and "
                        + player_table.get(
                            doc_id=matchs_for_a_tournament[match - 1]["match"][0][0]
                        )["first_name"]
                        + " "
                        + player_table.get(
                            doc_id=matchs_for_a_tournament[match - 1]["match"][0][0]
                        )["last_name"]
                        + " drew\n",
                    )
            matchs = "".join(matchs_of_round)
            rounds_for_a_tournament_for_print[i].append(matchs)
            i += 1

        print(
            tabulate(
                rounds_for_a_tournament_for_print,
                headers=[
                    "Name",
                    "Start date",
                    "End date",
                    "Match",
                ],
                tablefmt="fancy_grid",
            )
        )

    def display_choice_tournament_for_print_matchs(self):
        choice_tournament = input(
            "For which tournament do you want to display matchs (choose an id): "
        )
        return choice_tournament

    def display_matchs_for_a_tournament(self, choice_tournament):
        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        player_table = db.table("player")
        round_table = db.table("round")
        match_table = db.table("match")
        chooses_tournament = tournament_table.all()[int(choice_tournament) - 1]
        matchs_for_a_tournament = []
        for round in chooses_tournament["rounds"]:
            for match in round_table.all()[round - 1]["list_of_match"]:
                matchs_for_a_tournament.append(match_table.all()[match - 1])
        matchs_for_a_tournament_to_print = []
        for match in matchs_for_a_tournament:
            if match["match"][0][1] == 1.0 and match["match"][1][1] == 0.0:
                matchs_for_a_tournament_to_print.append(
                    [
                        match.doc_id,
                        player_table.get(doc_id=match["match"][0][0])["first_name"]
                        + " "
                        + player_table.get(doc_id=match["match"][0][0])["last_name"]
                        + " won against "
                        + player_table.get(doc_id=match["match"][1][0])["first_name"]
                        + " "
                        + player_table.get(doc_id=match["match"][1][0])["last_name"],
                    ]
                )
            elif match["match"][0][1] == 0.0 and match["match"][1][1] == 1.0:
                matchs_for_a_tournament_to_print.append(
                    [
                        match.doc_id,
                        player_table.get(doc_id=match["match"][1][0])["first_name"]
                        + " "
                        + player_table.get(doc_id=match["match"][1][0])["last_name"]
                        + " won against "
                        + player_table.get(doc_id=match["match"][0][0])["first_name"]
                        + " "
                        + player_table.get(doc_id=match["match"][0][0])["last_name"],
                    ]
                )
            elif match["match"][0][1] == 0.5 and match["match"][1][1] == 0.5:
                matchs_for_a_tournament_to_print.append(
                    [
                        match.doc_id,
                        player_table.get(doc_id=match["match"][1][0])["first_name"]
                        + " "
                        + player_table.get(doc_id=match["match"][1][0])["last_name"]
                        + " and "
                        + player_table.get(doc_id=match["match"][0][0])["first_name"]
                        + " "
                        + player_table.get(doc_id=match["match"][0][0])["last_name"]
                        + " drew",
                    ]
                )

        print(
            tabulate(
                matchs_for_a_tournament_to_print,
                headers=["Id", "Match"],
                tablefmt="fancy_grid",
            )
        )

    def display_ranking_menu(self):
        """ """
        menu_choice = input(
            "=========="
            "\n"
            "\nWhat do you want to do :\n"
            "  1 - Change ranking\n"
            "  2 - Go to main menu\n"
        )

        return menu_choice

    def choice_player_to_change_ranking(self):
        choice_player = input(
            "For which player do you want to change ranking (choose an id): "
        )
        return choice_player

    def display_players_menu(self):
        """ """
        menu_choice = input(
            "  1 - Display players by ranking\n"
            "  2 - Display players by alphabetical order\n"
            "  3 - Change ranking\n"
            "  4 - Go to main menu\n"
            "  5 - Quit\n"
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
                tablefmt="fancy_grid",
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
                    "Ranking",
                    "Id",
                    "First name",
                    "Last name",
                    "Date of birth",
                    "Gender",
                ],
                tablefmt="fancy_grid",
            )
        )

    def display_players_by_ranking_menu(self):
        """ """
        # print("")
        menu_choice = input(
            "  1 - Display players by alphabetical order\n"
            "  2 - Change ranking\n"
            "  3 - Go to main menu\n"
            "  4 - Quit\n"
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
        players = sorted(players, key=lambda k: (k[0], k[1]))
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
                tablefmt="fancy_grid",
            )
        )

    def display_players_by_alphabetical_order_menu(self):
        """ """
        # print("")
        menu_choice = input(
            "  1 - Display players by ranking\n"
            "  2 - Change ranking\n"
            "  3 - Go to main menu\n"
            "  4 - Quit\n"
        )

        return menu_choice

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
                    "Id",
                    "First name",
                    "Last name",
                    "Ranking",
                    "Date of birth",
                    "Gender",
                ],
                tablefmt="fancy_grid",
            )
        )

    def display_remaining_players_by_id(self, list_of_remaining_players):
        """ """
        players = []
        for player in list_of_remaining_players:
            players.append(
                [
                    player[0],
                    player[1],
                    player[2],
                    player[3],
                    player[4],
                    player[5],
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
                    "Ranking",
                    "Date of birth",
                    "Gender",
                ],
                tablefmt="fancy_grid",
            )
        )

    def display_write_score_menu(self, match):
        """ """
        db = TinyDB("db.json")
        player_table = db.table("player")
        menu_choice = input(
            "\n"
            "\nWho win :\n"
            "  1 - "
            + player_table.get(doc_id=match["match"][0][0])["first_name"]
            + " "
            + player_table.get(doc_id=match["match"][0][0])["last_name"]
            + " win\n"
            "  2 - "
            + player_table.get(doc_id=match["match"][1][0])["first_name"]
            + " "
            + player_table.get(doc_id=match["match"][1][0])["last_name"]
            + " win\n"
            "  3 - Draw match\n"
        )

        return menu_choice

    def display_players_by_score(self):
        """ """
        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        player_table = db.table("player")
        players = []
        for player in tournament_table.all()[-1]["players"]:
            players.append(
                [
                    player_table.all()[player - 1].doc_id,
                    player_table.all()[player - 1]["score"],
                    player_table.all()[player - 1]["ranking"],
                    player_table.all()[player - 1]["last_name"],
                    player_table.all()[player - 1]["first_name"],
                    player_table.all()[player - 1]["date_of_birth"],
                    player_table.all()[player - 1]["gender"],
                ]
            )
        players = sorted(
            players, key=lambda player: (player[1], -player[2]), reverse=True
        )
        print(
            tabulate(
                players,
                headers=[
                    "Id",
                    "Score",
                    "Ranking",
                    "First name",
                    "Last name",
                    "Date of birth",
                    "Gender",
                ],
                tablefmt="fancy_grid",
            )
        )

    def display_choice_add_players_create_tournament(self):
        menu_choice = input(
            "\n  1 - Add existed players\n"
            "  2 - Add a new player\n"
            "  3 - Change ranking\n"
        )
        return menu_choice

    def display_remaining_players_to_add(self, number_of_player):
        print("\n" + str(8 - number_of_player) + " players remaining\n")

    def display_warning_add_a_player_several_time(self):
        print("Player alredy choosen. Please add an other player\n")

    def display_match_information(self):
        db = TinyDB("db.json")
        player_table = db.table("player")
        match_table = db.table("match")
        round_table = db.table("round")
        matchs_for_a_round = []
        matchs_for_a_round_to_print = []
        black_or_white_player = []
        for match in round_table.all()[-1]["list_of_match"]:
            matchs_for_a_round.append(match_table.all()[match - 1])
        for match in matchs_for_a_round:
            black_or_white_player.append(
                [
                    str(player_table.get(doc_id=match["match"][0][0])["first_name"])
                    + " "
                    + str(player_table.get(doc_id=match["match"][0][0])["last_name"]),
                    str(player_table.get(doc_id=match["match"][1][0])["first_name"])
                    + " "
                    + str(player_table.get(doc_id=match["match"][1][0])["last_name"]),
                ]
            )
            matchs_for_a_round_to_print.append(match)
        print(
            tabulate(
                black_or_white_player,
                headers=[
                    "Black",
                    "White",
                ],
                tablefmt="fancy_grid",
            )
        )

    def display_message_first_round_create(self):
        print("\nMatchs of round 1 : ")

    def display_message_other_round_create(self, round_number):
        print("Round " + str(round_number) + " has been created")

    def display_warning_players_same_ranking(self, new_ranking):
        print(
            "At least 2 players have "
            + str(new_ranking)
            + " as ranking. Please modify ranking"
        )

    def quit(self):
        """
        Display a thank you message when the user qui the program
        """
        print("\nClosing the program...\n")
