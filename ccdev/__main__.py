import os

from ccdev import ProjectHome
from ccdev.command_line_app import CommandFactory, CommandLineSQLTaskApp


def main():
    app = CommandLineSQLTaskApp(
        args_factory=CommandFactory(ProjectHome(os.getcwd(), os.environ))
    )
    app.run()


if __name__ == "__main__":
    main()
