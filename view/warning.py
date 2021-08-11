from tinydb import TinyDB

from model.player import Player


class WarningView:
    def __init__(
        self,
        tournament_table=TinyDB("db.json").table("tournament"),
        player_table=TinyDB("db.json").table("player"),
    ):
        self.tournament_table = tournament_table
        self.player_table = player_table

    def welcome_message(self):
        print("\n" "Welcome to Ultimate Chess Manager")

    def remaining_players_to_add(self, number_of_player):
        print("\n" + str(8 - number_of_player) + " players remaining\n")

    def add_a_player_several_time(self):
        print("\n Player already choosen. Please add an other player\n")

    def round_create(self, round_number):
        print("\n Round " + str(round_number) + " has been created")

    def players_same_ranking(self, new_ranking):
        print(
            "\n At least 2 players have "
            + str(new_ranking)
            + " as ranking. Please modify ranking"
        )

    def no_tournament(self):
        print("\n No tournament available")

    def no_player(self):
        print("\n No player available")

    def tournament_winner(self):
        players_of_tournament_by_score = []
        players_of_tournament = [
            self.player_table.all()[players - 1]
            for players in self.tournament_table.all()[-1]["players"]
        ]
        players_of_tournament_by_score = Player.sort_list_of_players_by_score(
            self, players_of_tournament
        )
        print(
            "\n The winner is "
            + players_of_tournament_by_score[0]["first_name"]
            + " "
            + players_of_tournament_by_score[0]["last_name"]
        )

    def quit(self):
        """
        Display a thank you message when the user quit the program
        """
        print("\nClosing the program...\n")
