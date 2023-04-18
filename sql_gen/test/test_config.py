import tempfile
from pathlib import Path

import pytest

from sql_gen.config import ConfigFile


class PropertiesFileGenerator(object):
    def __init__(self, properties={}):
        if type(properties) == str:
            properties = self._to_dict(properties)
        self.config = properties

    def _to_dict(self, config_content):
        dict = {}
        for line in config_content.splitlines():
            k, v = line.split("=")
            dict[k] = v
        return dict

    def put(self, property_name, property_value):
        self.config[property_name] = property_value

    def save(self, filepath):
        filepath.write_text(self._convert_to_text())

    def _convert_to_text(self):
        str_builder = []
        for k, v in self.config.items():
            if str_builder:
                str_builder.append("\n")

            str_builder.append(f"{k}={v}")
        return "".join(str_builder)


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
    config_file = ConfigFile(filepath)

    assert len(properties) == len(config_file)
    for k, v in properties.items():
        assert v == config_file[k]


class PropertiesFolderGenerator(object):
    def __init__(self):
        self.file_generators = {}

    def add_properties_file(self, key, properties_dict):
        self.file_generators[key] = PropertiesFileGenerator(properties_dict)

    def save(self, destination):
        for key, file_generator in self.file_generators.items():
            file_generator.save(Path(destination) / self._get_file_name(key))

    def _get_file_name(self, key):
        return key


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
    return ConfigFile(config_home)


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


def test_it_resolve_value_assigned_to_var_multiple_times_no_matter_the_order():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        config_content = "db.user=${db.name}\ndb.name=${ad.name}\nad.name=DEV"
        config = make_config(config_content, tmpdirpath)
        assert "DEV" == config["db.user"]


def test_get_config_value_when_no_file_exist_throws_exception():
    config_home = "/em/project/gsc/config/emautomation.properties"
    fake_logger = FakeLogger()
    with pytest.raises(FileNotFoundError) as excinfo:
        config = ConfigFile(config_home, fake_logger)
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
