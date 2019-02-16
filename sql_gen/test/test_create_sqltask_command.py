from sql_gen.create_sqltask_command import CreateSQLTaskCommand
import pytest

class FakeWriter(object):
    def __init__(self):
        self.content=""

    def write(self,content):
        self.content = content

#def test_if_sqltask_exist_and_user_not_confirm_then_it_doesnt_run():

@pytest.mark.skip
def test_writes_sqltask():
    consolewritter =FakeWriter()
    outputwriter_factory = OuputWriterFactory()
    app = CreateSQLTaskCommand(outputwriter_factory)
    app.set_path(path)
    app.set_path(None)

    app.run()

    assert "hello" == consolewritter.content

@pytest.mark.skip
def test_dir_passed_ouputs_to_file():
    filewriter = FileWriter()
    path = "modules/my_module"
    outputwriter_factory = OuputWriterFactory()
    app = CreateSQLTaskCommand(outputwriter_factory)
    app.set_path(path)

    app.run()

    assert "modules/my_module" == filewriter.path
    assert "hello" == filewriter.content


