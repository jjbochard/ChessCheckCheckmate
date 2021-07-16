from tinydb import TinyDB


class SelectMenuView:
    def __init__(
        self,
        tournament_table=TinyDB("db.json").table("tournament"),
        player_table=TinyDB("db.json").table("player"),
        round_table=TinyDB("db.json").table("round"),
        match_table=TinyDB("db.json").table("match"),
    ):
        self.tournament_table = tournament_table
        self.player_table = player_table
        self.round_table = round_table
        self.match_table = match_table

    def main_menu(self):
        if (
            self.tournament_table.all() == []
            or self.tournament_table.all()[-1]["status_tournament"] == "finished"
        ):
            menu_choice = input(
                "\n"
                "  1 - Start a tournament\n"
                "  2 - Create a player\n"
                "  3 - Change ranking\n"
                "  4 - Display tournaments\n"
                "  5 - Display players\n"
                "  6 - Quit\n"
            )
        else:
            menu_choice = input(
                "\n"
                "  1 - Continue a tournament\n"
                "  2 - Create a player\n"
                "  3 - Change ranking\n"
                "  4 - Display tournaments\n"
                "  5 - Display players\n"
                "  6 - Quit\n"
            )
        return menu_choice

    def tournament_menu(self):
        menu_choice = input(
            "  1 - Display tournament's players\n"
            "  2 - Display tournament's rounds\n"
            "  3 - Display tournament's matchs\n"
            "  4 - Change ranking\n"
            "  5 - Go to main menu\n"
            "  6 - Quit\n"
        )
        return menu_choice

    def next_round_menu(self):
        menu_choice = input(
            "\n"
            "  1 - Create next round\n"
            "  2 - Change ranking\n"
            "  3 - Go to main menu\n"
            "  4 - Quit\n"
        )
        return menu_choice

    def end_round_menu(self):
        menu_choice = input(
            "\n" "  1 - End round\n" "  2 - Go to main menu\n" "  3 - Quit\n"
        )
        return menu_choice

    def print_players_menu(self):
        choice_manner = input(
            "\n"
            "  1 - Display players by ranking\n"
            "  2 - Display players by alphabetical order\n"
        )
        return choice_manner

    def players_by_ranking_menu(self):
        menu_choice = input(
            "  1 - Display players by alphabetical order\n"
            "  2 - Change ranking\n"
            "  3 - Go to main menu\n"
            "  4 - Quit\n"
        )
        return menu_choice

    def players_by_alphabetical_order_menu(self):
        menu_choice = input(
            "  1 - Display players by ranking\n"
            "  2 - Change ranking\n"
            "  3 - Go to main menu\n"
            "  4 - Quit\n"
        )
        return menu_choice

    def ranking_menu(self):
        menu_choice = input(
            "\n"
            "\nWhat do you want to do :\n"
            "  1 - Change ranking\n"
            "  2 - Go to main menu\n"
        )
        return menu_choice

    def players_menu(self):
        menu_choice = input(
            "  1 - Display players by ranking\n"
            "  2 - Display players by alphabetical order\n"
            "  3 - Change ranking\n"
            "  4 - Go to main menu\n"
            "  5 - Quit\n"
        )
        return menu_choice

    def write_score_menu(self, match):
        menu_choice = input(
            "\n"
            "\nWho win :\n"
            "  1 - "
            + self.player_table.get(doc_id=match["player_1"])["first_name"]
            + " "
            + self.player_table.get(doc_id=match["player_1"])["last_name"]
            + " win\n"
            "  2 - "
            + self.player_table.get(doc_id=match["player_2"])["first_name"]
            + " "
            + self.player_table.get(doc_id=match["player_2"])["last_name"]
            + " win\n"
            "  3 - Draw match\n"
        )
        return menu_choice

    def add_player_create_tournament_menu(self):
        menu_choice = input(
            "\n  1 - Add existed players\n"
            "  2 - Add a new player\n"
            "  3 - Change ranking\n"
        )
        return menu_choice

    def change_ranking(self):
        choice_player = input(
            "For which player do you want to change ranking (choose an id): "
        )
        return choice_player

    def add_player(self):
        choice_player = input(
            "Which player do you want to add to this tournament (choose an id): "
        )
        return choice_player

    def choose_tournament_for_print_players(self):
        choice_tournament = input(
            "For which tournament do you want to display players (choose an id): "
        )
        return choice_tournament

    def choose_tournament_for_print_rounds(self):
        choice_tournament = input(
            "For which tournament do you want to display rounds (choose an id): "
        )
        return choice_tournament

    def choose_tournament_for_print_matchs(self):
        choice_tournament = input(
            "For which tournament do you want to display matchs (choose an id): "
        )
        return choice_tournament
