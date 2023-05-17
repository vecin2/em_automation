import os

from sqltask.main.default_app_config import DefaultAppContainer


def main():

    # app = CommandLineSQLTaskApp.build_app(os.getcwd(), os.environ)
    app = DefaultAppContainer().resolve(os.getcwd(), os.environ)
    app.run()


if __name__ == "__main__":
    main()
