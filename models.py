class Tournament:
    def __init__(
        self,
        name,
        place,
        start_date,
        end_date,
        nb_of_rounds,
        list_of_rounds,
        players,
        time_control,
        description,
    ):

        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.nb_of_rounds = nb_of_rounds
        self.list_of_rounds = list_of_rounds
        self.players = players
        self.time_control = time_control
        self.description = description

    @classmethod
    def create_tournament(cls):
        print(
            "Welcome in the beautiful application.\nPlease enter all the informations about the new \
                tournament you want to start."
        )
        return cls(
            input("Name: "),
            input("Place: "),
            input("Start date: "),
            input("End date: "),
            int(input("Number of rounds: ")),
            [1, 2],
            [],
            input("Time control: "),
            input("Description: "),
        )


class Player:
    def __init__(
        self, first_name, last_name, date_of_birth, gender, ranking, nb_of_points
    ):
        self.first_name = (first_name,)
        self.last_name = (last_name,)
        self.date_of_birth = (date_of_birth,)
        self.gender = (gender,)
        self.ranking = (ranking,)
        self.nb_of_points = nb_of_points


class Match:
    def __init__(self, player_1, player_2, result_player_1, result_player_2):
        self.player_1 = (player_1,)
        self.player_2 = (player_2,)
        self.result_player_1 = (result_player_1,)
        self.result_player_2 = result_player_2


class Round:
    def __init__(self, list_of_match):
        self.list_of_match = list_of_match
