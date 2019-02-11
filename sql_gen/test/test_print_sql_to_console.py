from sql_gen.print_sql_to_console_command import PrintSQLToConsoleCommand,PrintSQLToConsoleDisplayer


def test_it_sends_to_console_the_filled_template(mocker):
    sql_output = "hello Mark"
    displayer = PrintSQLToConsoleDisplayer()
    mocker.patch.object(displayer,'render_sql')
    command = PrintSQLToConsoleCommand(displayer)
    command.run()
    displayer.render_sql.assert_called_once_with(sql_output)
