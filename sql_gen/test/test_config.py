from sql_gen.exceptions import ConfigFileNotFoundException
from sql_gen.config import ConfigFile
import pytest

class FakeLogger(object):
    def __init__(self):
        self.debug_text=""
        self.error_text=""
    def debug(self,text):
        self.debug_text +=text

    def error(self,exception):
        if isinstance(exception,Exception):
            self.error_text +=str(exception.value)
        else:
            self.error_text +=exception

def make_config(fs,config_content,config_home=None):
    if not config_home:
        config_home ="/em/project/gsc/config/emautomation.properties"
    fs.create_file(config_home,contents=config_content)
    return ConfigFile(config_home)

def test_get_config_value_returns_value(fs):
    config_content="container.name=ad"
    config = make_config(fs,config_content)
    assert "ad" == config["container.name"]

def test_it_throws_exception_when_value_cannot_be_resolved(fs):
    config_content="database.user=${logical.db.name}"
    config = make_config(fs,config_content)
    with pytest.raises(Exception) as excinfo:
        config["database.user"]
    assert "Bad value substitution" in  str(excinfo)

def test_it_resolve_value_assigned_to_var_multiple_times(fs):
    config_content="ad.name=DEV\ndb.name=${ad.name}\ndb.user=${db.name}"
    config = make_config(fs,config_content)
    assert "DEV" == config["db.user"]

def test_it_resolve_value_assigned_to_var_concatenated_with_string(fs):
    config_content="ad.name=DEV\ndb.name=${ad.name}_RS\n"
    config = make_config(fs,config_content)
    assert "DEV_RS" == config["db.name"]

def test_it_resolve_value_assigned_to_var_multiple_times_no_matter_the_order(fs):
    config_content="db.user=${db.name}\ndb.name=${ad.name}\nad.name=DEV"
    config = make_config(fs,config_content)
    assert "DEV" == config["db.user"]

def test_get_config_value_when_no_file_exist_throws_exception():
    config_home ="/em/project/gsc/config/emautomation.properties"
    fake_logger = FakeLogger()
    with pytest.raises(FileNotFoundError) as excinfo:
        config = ConfigFile(config_home,fake_logger)
        config.properties
    assert "Try to load config file '"+config_home+"' but it does not exist" in  str(excinfo)

