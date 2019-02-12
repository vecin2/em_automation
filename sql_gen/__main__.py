from sql_gen import sqltaskapp
from sql_gen.command_factory import CommandFactory 
from sql_gen.command_line_app import CommandLineSQLTaskApp
##main
def main():
    #sqltaskapp.init()
    #sqltaskapp.run()
    app_test_factory = CommandFactory()
    app = CommandLineSQLTaskApp(app_test_factory)
    app.run()


if __name__ == '__main__':
    main()

