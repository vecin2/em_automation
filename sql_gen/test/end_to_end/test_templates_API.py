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

def test_query_runner(app_runner):
    #fs.create_dir("/opt/em/projects/Pacificorp/trunk")
    #content="{{ verb_names | _addb."
    #content ="v__by_id=SELECT * FROM eva_verb where id= 2129"
    #fs.create_file("/em/project/sqltask/config/ad_queries.sql",
    #                contents=content)
    #env_vars={'EM_CORE_HOME':'/em/project'}
    app = AppProject(os.environ)
    app_runner.with_emproject_under("/opt/em/projects/Pacificorp/trunk")\
              .saveAndExit()\
              .run_prod()
    #query_runner = QueryRunner.make_from_app_prj(app)
    #assert str([1233]) == str(query_runner.list.v__by_id)
