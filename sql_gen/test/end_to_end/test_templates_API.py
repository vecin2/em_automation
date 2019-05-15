import os
import pytest

from sql_gen.test.utils.app_runner import PrintSQLToConsoleAppRunner
from sql_gen.app_project import AppProject
from sql_gen.emproject import QueryRunner

@pytest.fixture
def app_runner():
    app_runner = PrintSQLToConsoleAppRunner()
    yield app_runner
    app_runner.teardown()

#disabled because is a computer specific test. We need to test this part with unit tests
@pytest.mark.skip
def test_query_runner(app_runner):
    app = AppProject(os.environ)
    app_runner.with_emproject_under("/opt/em/projects/Pacificorp/trunk")\
              .saveAndExit()\
              .run_prod()
