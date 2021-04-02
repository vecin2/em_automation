import pytest
from sql_gen.app_project import AppProject
from sql_gen.emproject import EMProject, EMConfigID
from sql_gen.test.utils.emproject_test_util import FakeEMProjectBuilder
import os


class FakeAppPrjBuilder(object):
    def __init__(self, emproject, fs, env_vars=None):
        self.emproject = emproject
        self.app_project = AppProject(env_vars=env_vars)
        self.fs = fs

    def add_config(self, content):
        self._add_file(self.app_project.paths["core_config"].path, content)
        return self

    def set_ad_queries(self, content):
        self._add_file(self.app_project.paths["ad_queries"].path, content)
        return self

    def _add_file(self, prj_path, content):
        full_path = os.path.join(self.app_project.root, prj_path)
        self.fs.create_file(full_path, contents=content)
        return self

    def build(self):
        return self.app_project


def test_instantiate_ad_queryrunner(fs):
    emconfig_content = """
database.user=sa
database.pass=admin
database.host=localhost
database.port=1433
database.name=ootb_15_1_fp2
database.type=sqlServer
"""
    em_project_home = "/home/em/my_project"
    config_id = EMConfigID("localdev", "localhost", "ad")
    env_vars = {"EM_CORE_HOME": "/home/em/my_project"}
    em_project = (
        FakeEMProjectBuilder(fs, em_project_home)
        .add_config(config_id, emconfig_content)
        .build()
    )
    config_content = """
environment.name=localdev
machine.name=localhost
container.name=ad
"""
    queries_content = """
v_names__by_ed=SELECT * FROM verb_name WHERE NAME='{}'"""
    prj = (
        FakeAppPrjBuilder(em_project, fs, env_vars)
        .add_config(config_content)
        .set_ad_queries(queries_content)
        .build()
    )
    assert prj.ad_queryrunner.has_query("v_names__by_ed")
