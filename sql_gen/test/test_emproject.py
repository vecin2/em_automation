from sql_gen.emproject import EMProject
from sql_gen.test.utils.emproject_test_util import FakeEMProjectBuilder
import pytest

def prj_builder(fs, root='/home/em'):
    return FakeEMProjectBuilder(fs,root)

@pytest.mark.skip
def test_config(fs):
    config_id = EMConfigID("localdev",
                       "localhost",
                       "ad")
    prj_builder(fs).add_config_settings(config_id, {"db.host":"localhost"})

    project = EMProject('/home/emproject')
    #project.config(local)
