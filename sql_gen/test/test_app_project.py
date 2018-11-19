import pytest
from sql_gen.app_project import AppProject
from sql_gen.emproject import EMProject,EMConfigID
from sql_gen.test.utils.emproject_test_util import FakeEMProjectBuilder
import os

class FakeAppPrjBuilder(object):

    def __init__(self,emproject,fs):
        self.emproject= emproject
        self.app_project =AppProject(emproject)
        self.fs =fs

    def add_config(self,content):
        self._add_file(self.app_project.paths["core_config"],content)
        return self

    def set_ad_queries(self,content):
        self._add_file(self.app_project.paths["ad_queries"],content)
        return self


    def _add_file(self,prj_path,content):
        full_path = os.path.join(self.app_project.root, prj_path)
        self.fs.create_file(full_path,contents=content)
        return self

    def build(self):
        return self.app_project

def test_instantiate_defaults_to_em_core_home():
    prj = AppProject()
    assert os.path.join(os.environ["EM_CORE_HOME"],"sqltask")==prj.root

def test_instantiate_with_emproject(fs):
    emproject = EMProject("/home/em/my_project")
    prj = AppProject(emproject)
    assert "/home/em/my_project/sqltask" ==prj.root

def test_instantiate_ad_queryrunner(fs):
    emconfig_content="""
database.admin.user=sa
database.admin.pass=admin
database.host=localhost
database.port=1433
database.name=ootb_15_1_fp2
database.type=sqlServer
"""
    em_project_home="/home/em/my_prj"
    config_id = EMConfigID("localdev","localhost","ad")
    em_project  = FakeEMProjectBuilder(fs,em_project_home)\
                    .add_config(config_id,emconfig_content)\
                    .build()
    config_content="""
environment.name=localdev
machine.name=localhost
container.name=ad
"""
    queries_content="""
v_names__by_ed=SELECT * FROM verb_name WHERE NAME='{}'"""
    prj = FakeAppPrjBuilder(em_project,fs)\
                    .add_config(config_content)\
                    .set_ad_queries(queries_content)\
                    .build()
    assert prj.ad_queryrunner.has_query("v_names__by_ed")

