from controller import Controller
from view.select_menu import SelectMenuView
from view.tables import TablesView
from view.warning import WarningView


def main():
    """
    Run the program
    """
    select = SelectMenuView()
    table = TablesView()
    warning = WarningView()

    program_controller = Controller(select, table, warning)
    program_controller.run()


if __name__ == "__main__":
    main()
