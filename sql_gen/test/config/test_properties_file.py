import tempfile
from pathlib import Path

import pytest

from sql_gen.config import PropertiesFile
from sql_gen.test.config.utils import PropertiesFileGenerator


def test_properties_file_generator():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        properties = {}
        properties["preferred.default.locale"] = "en-GB"
        properties["database.host"] = "ad"
        config_generator = PropertiesFileGenerator(properties)

        path = Path(tmpdirpath) / "test.properties"
        config_generator.save(path)

        assert_equal_properties(properties, path)


def assert_equal_properties(properties, filepath):
    config_file = PropertiesFile(filepath)

    assert len(properties) == len(config_file)
    for k, v in properties.items():
        assert v == config_file[k]


class FakeLogger(object):
    def __init__(self):
        self.debug_text = ""
        self.error_text = ""

    def debug(self, text):
        self.debug_text += text

    def error(self, exception):
        if isinstance(exception, Exception):
            self.error_text += str(exception.value)
        else:
            self.error_text += exception


def make_config(config_content, config_home=None):
    config_home = Path(config_home) / "some.properties"
    PropertiesFileGenerator(config_content).save(config_home)
    return PropertiesFile(config_home)


def test_get_config_value_returns_value():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        config_content = "container.name=ad"
        config = make_config(config_content, tmpdirpath)
        assert "ad" == config["container.name"]


def test_it_resolve_value_assigned_to_var_multiple_times():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        config_content = "ad.name=DEV\ndb.name=${ad.name}\ndb.user=${db.name}"
        config = make_config(config_content, tmpdirpath)
        assert "DEV" == config["db.user"]


def test_it_resolve_value_assigned_to_var_multiple_times_no_matter_the_order():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        config_content = "db.user=${db.name}\ndb.name=${ad.name}\nad.name=DEV"
        config = make_config(config_content, tmpdirpath)
        assert "DEV" == config["db.user"]


def test_duplicate_property_takes_last_value_assigned():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        config_content = "home=/em/prj\nhome=/opt/appserver"
        config = make_config(config_content, tmpdirpath)
        assert "/opt/appserver" == config["home"]


def test_it_throws_exception_when_value_cannot_be_resolved():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        config_content = "database.user=${logical.db.name}"
        config = make_config(config_content, tmpdirpath)
        with pytest.raises(Exception) as excinfo:
            config["database.user"]
        assert "Bad value substitution" in str(excinfo)


def test_it_resolve_value_assigned_to_var_concatenated_with_string():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        config_content = "ad.name=DEV\ndb.name=${ad.name}_RS\n"
        config = make_config(config_content, tmpdirpath)
        assert "DEV_RS" == config["db.name"]


def test_get_config_value_when_no_file_exist_throws_exception():
    config_home = "/em/project/gsc/config/emautomation.properties"
    fake_logger = FakeLogger()
    with pytest.raises(FileNotFoundError) as excinfo:
        config = PropertiesFile(config_home, fake_logger)
        config.properties
    assert "Try to load config file '" + config_home + "' but it does not exist" in str(
        excinfo
    )


@pytest.mark.skip
def test_config_dict():
    with tempfile.TemporaryDirectory() as tmp_project_root:
        config_generator.put("ad", {"preferred.default.locale": "en-GB"})
        config_generator.app.put("app", {"environment.name": "localdev"})
        project_config = ProjectConfig(tmp_project_root)
        assert "ad" == project_config.app["environment.name"]
        assert "ad" == project_config.em["ad"]["enviornment.name"]
