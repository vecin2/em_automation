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


def test_get_config_value_returns_value(fs):
    config_home ="/em/project/gsc/config/emautomation.properties"
    config_content="container.name=ad"
    fs.create_file(config_home,contents=config_content)
    config = ConfigFile(config_home)
    assert "ad" == config["container.name"]

def test_get_config_value_when_no_file_exist_throws_exc_and_logs_it(fs):
    config_home ="/em/project/gsc/config/emautomation.properties"
    fake_logger = FakeLogger()
    with pytest.raises(ConfigFileNotFoundException) as e_info:
        config = ConfigFile(config_home,fake_logger)
    assert "File not found" in fake_logger.error_text
