from controllers import Controller
from views import View


def main():
    """
    Run the program
    """
    view = View()

    program_controller = Controller(view)
    program_controller.run()


if __name__ == "__main__":
    main()
