import os

from ccdev.command_line_app import CommandLineSQLTaskApp


def main():

    app = CommandLineSQLTaskApp.build_app(os.getcwd(), os.environ)
    app.run()


if __name__ == "__main__":
    main()
