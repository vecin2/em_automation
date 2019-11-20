import pytest

from sql_gen.test.utils.app_runner import AppRunner
class DevtaskAppRunner(AppRunner):
    def __init__(self,fs=None):
        super().__init__(fs=fs)

@pytest.fixture
def app_runner(fs):
    app_runner = DevtaskAppRunner(fs)
    yield app_runner
    app_runner.teardown()

@pytest.mark.skip 
def test_invalid_path_shows_error_msg(app_runner,fs):
    otb_process ="/FrameworkCaseHandling/Implementation/Case/Processes/CancelCaseCreation"
    fs.create_file("/templates/extend_verb.sql")
    app_runner.using_templates_under("/templates")\
              .saveAndExit()\
              .run()
              #.assert_displayed_error("No such process '"+otb_process+"'")
