import pytest

from sql_gen.test.utils.app_runner import TemplatesAppRunner
from sql_gen.exceptions import EnvVarNotFoundException

@pytest.fixture
def app_runner(fs):
    app_runner = TemplatesAppRunner(fs=fs)
    yield app_runner
    app_runner.teardown()


@pytest.mark.skip
def test_render_sql_matches_expected_sql(app_runner,fs):
    app_runner.with_emproject_under("/em/prj")\
               .and_prj_built_under("/em/prj")\
               .add_template("greeting.sql","hello {{name}}!")\
               .add_test("test_greeting.sql",
                         {'name': 'David'},
                         "hello Davids!")\
               .run()\
