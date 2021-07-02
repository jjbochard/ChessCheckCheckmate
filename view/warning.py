from tinydb import TinyDB


class WarningView:
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

    def welcome_message(self):
        """ """
        welcome_message = print(
            "\n" "====================\n" "\n" "Welcome to Ultimate Chess Manager" "\n"
        )
        return welcome_message

    def remaining_players_to_add(self, number_of_player):
        print("\n" + str(8 - number_of_player) + " players remaining\n")

    def add_a_player_several_time(self):
        print("Player alredy choosen. Please add an other player\n")

    def round_create(self, round_number):
        print("Round " + str(round_number) + " has been created")

    def players_same_ranking(self, new_ranking):
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
