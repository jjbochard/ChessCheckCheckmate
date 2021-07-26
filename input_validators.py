from datetime import datetime

from tinydb import TinyDB

from model import Player, Tournament


def is_valid_main_menu_response(response):
    if response in ["1", "2", "3", "4", "5", "6"]:
        return True


def is_valid_tournament_menu_response(response):
    if response in ["1", "2", "3", "4", "5", "6"]:
        return True


def is_valid_next_round_menu_response(response):
    if response in ["1", "2", "3"]:
        return True


def is_valid_end_round_menu_response(response):
    if response in ["1", "2", "3"]:
        return True


def is_valid_print_players_menu_response(response):
    if response in ["1", "2"]:
        return True


def is_valid_players_by_ranking_menu_response(response):
    if response in ["1", "2", "3", "4"]:
        return True


def is_valid_players_by_alphabetical_order_menu_response(response):
    if response in ["1", "2", "3", "4"]:
        return True


def is_valid_ranking_menu_response(response):
    if response in ["1", "2"]:
        return True


def is_valid_players_menu_response(response):
    if response in ["1", "2", "3", "4", "5"]:
        return True


def is_valid_write_score_menu_response(response):
    if response in ["1", "2", "3"]:
        return True


def is_valid_add_player_create_tournament_menu_response(response):
    if response in ["1", "2", "3"]:
        return True


def is_valid_time_control(response):
    if response not in ["Blitz", "Bullet", "Rapid"]:
        print("  Time control must be Blitz, Bullet or Rapid")
    else:
        return True


def is_valid_gender(response):
    if response not in ["Female", "Male"]:
        print("  Gender must be Female or Male")
    else:
        return True


def is_valid_id_player(response):
    list_players = Player.get_players(TinyDB("db.json").table("player"))
    if response not in list_players:
        print("  Invalid player Id")
    else:
        return True


def is_valid_id_tournament(response):
    list_tournaments = Tournament.get_tournaments(TinyDB("db.json").table("tournament"))
    if response not in list_tournaments:
        print("  Invalid tournamanet Id")
    else:
        return True


def is_unused_ranking(response):
    list_rankings = Player.get_rankings(TinyDB("db.json").table("player"))
    list_rankings.append(response)
    contains_duplicates = any(
        list_rankings.count(element) > 1 for element in list_rankings
    )
    if contains_duplicates:
        print("  Ranking already choosen")
    else:
        return True


def is_not_already_added_player(
    first_name_response, last_name_response, date_of_birth_response
):
    list_full_name, list_date_of_birth = Player.get_full_name_and_date_of_birth(
        TinyDB("db.json").table("player")
    )
    new_fullname = "%s %s" % (first_name_response, last_name_response)
    new_date_of_birth = date_of_birth_response
    date_of_birth_of_full_name_duplicate = Player.check_full_name_duplicate(
        new_fullname, list_full_name, list_date_of_birth
    )
    if date_of_birth_of_full_name_duplicate == []:
        return True
    for date in date_of_birth_of_full_name_duplicate:
        if Player.check_date_duplicate(new_date_of_birth, date) is True:
            print("  Player already exist")
        else:
            return True


def is_tournament_already_exist(tournament_name_response):
    list_tournament = Tournament.get_tournament_name(
        TinyDB("db.json").table("tournament")
    )
    new_tournament_name = tournament_name_response
    if list_tournament == []:
        return True
    for tournament_name in list_tournament:
        if (
            Tournament.check_tournament_duplicate(new_tournament_name, tournament_name)
            is True
        ):
            print("  Tournament already exists")
        else:
            return True


def is_valid_date_of_birth():
    while True:
        try:
            date_of_birth = input("Date_of_birth (dd/mm/yyyy): ")
            datetime.strptime(date_of_birth, "%d/%m/%Y")
            break
        except ValueError:
            print(
                "  Incorrect format given for dates. They must be given like 'dd/mm/yyyy'"
            )
    return date_of_birth


def is_valid_end_tournament_menu_response(response):
    if response in ["1", "2", "3"]:
        return True
