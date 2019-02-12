from sql_gen.commands import PrintSQLToConsoleCommand,PrintSQLToConsoleDisplayer
from sql_gen.create_doc_from_multiple_templates_command import CreateDocumentFromMultipleTemplatesCommand


def test_it_sends_to_console_the_filled_template(mocker):
    displayer = PrintSQLToConsoleDisplayer()
    mocker.patch.object(displayer,'render_sql')
    doc_creator=mocker.Mock(spec=CreateDocumentFromMultipleTemplatesCommand)
    doc_creator.run.return_value ="hello Mark"
    command = PrintSQLToConsoleCommand(doc_creator,displayer)

    command.run()

    displayer.render_sql.assert_called_once_with("hello Mark")


