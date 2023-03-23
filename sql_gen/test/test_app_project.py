import os

from sql_gen.app_project import AppProject
from sql_gen.emproject import EMConfigID
from sql_gen.test.utils.emproject_test_util import FakeEMProjectBuilder


class FakeAppPrjBuilder(object):
    def __init__(self, emproject, fs):
        self.emproject = emproject
        self.app_project = AppProject(emprj_path=emproject.root)
        self.fs = fs

    def add_config(self, content):
        self._add_file(self.app_project.paths["core_config"].path, content)
        return self

    def set_ad_queries(self, content):
        self.fs.create_file(
            self.app_project.library().db_queries("ad"), contents=content
        )
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
database.type=oracle
"""
    em_project_home = "/home/em/my_project"
    config_id = EMConfigID("localdev", "localhost", "ad")
    em_project = (
        FakeEMProjectBuilder(fs, em_project_home)
        .add_config(config_id, emconfig_content)
        .build()
    )
    config_content = """
environment.name=localdev
machine.name=localhost
container.name=ad
sqltask.library.path='/library'
"""
    queries_content = """
v_names__by_ed=SELECT * FROM verb_name WHERE NAME='{}'"""
    prj = (
        FakeAppPrjBuilder(em_project, fs)
        .add_config(config_content)
        .set_ad_queries(queries_content)
        .build()
    )
    assert prj.ad_queryrunner.has_query("v_names__by_ed")
