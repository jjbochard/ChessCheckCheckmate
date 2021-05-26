def is_valid_welcome_menu_response(response):
    """
    Cheking if the welcome input is True or False to continue
    Otherwise the welcome message keeps repeating
    """
    if response in ["1", "2", "3", "4", "5", "6", "7"]:
        return True
    else:
        return False


def is_valid_display_tournaments_menu_response(response):
    """
    Cheking if the welcome input is True or False to continue
    Otherwise the welcome message keeps repeating
    """
    if response in ["1", "2", "3", "4", "5", "6"]:
        return True
    else:
        return False


def is_valid_display_tournaments_response(response):
    """
    Cheking if the welcome input is True or False to continue
    Otherwise the welcome message keeps repeating
    """
    if response in ["1", "2", "3", "4", "5"]:
        return True
    else:
        return False


def is_valid_display_players_menu_response(response):
    """
    Cheking if the welcome input is True or False to continue
    Otherwise the welcome message keeps repeating
    """
    if response in ["1", "2", "3", "4", "5"]:
        return True
    else:
        return False


def is_valid_display_players_by_ranking_menu_response(response):
    """
    Cheking if the welcome input is True or False to continue
    Otherwise the welcome message keeps repeating
    """
    if response in ["1", "2", "3", "4"]:
        return True
    else:
        return False


def is_valid_display_players_by_alphabetical_order_menu_response(response):
    """
    Cheking if the welcome input is True or False to continue
    Otherwise the welcome message keeps repeating
    """
    if response in ["1", "2", "3", "4"]:
        return True
    else:
        return False


def is_valid_display_choice_add_players_create_tournament_menu_response(response):
    """
    Cheking if the welcome input is True or False to continue
    Otherwise the welcome message keeps repeating
    """
    if response in ["1", "2", "3"]:
        return True
    else:
        return False


def is_valid_display_change_ranking_menu_response(response):
    """
    Cheking if the welcome input is True or False to continue
    Otherwise the welcome message keeps repeating
    """
    if response in ["1", "2"]:
        return True
    else:
        return False
