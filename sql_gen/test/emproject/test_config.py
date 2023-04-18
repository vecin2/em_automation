import tempfile
from pathlib import Path

import pytest

from sql_gen.emproject.config import EMConfigID, EMEnvironmentConfig
from sql_gen.test.test_config import (PropertiesFolderGenerator,
                                      assert_equal_properties)


class EMEnvironmentConfigGenerator(PropertiesFolderGenerator):
    def __init__(self, env_name=None, machine_name=None):
        super().__init__()
        self.env_name = env_name
        self.machine_name = machine_name
        self.config_path = None

    def generate_config(self):
        # same api as ccadmin client
        return self.save(self.config_path)

    def _get_file_name(self, key):
        return EMConfigID(self.env_name, self.machine_name, key).filename()


def test_properties_folder_generator():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        properties1 = {"preferred.default.locale": "en-GB"}
        properties2 = {"database.port": "1521"}
        config_generator = PropertiesFolderGenerator()
        config_generator.add_properties_file("test1.properties", properties1)
        config_generator.add_properties_file("test2.properties", properties2)
        config_generator.save(tmpdirpath)
        path = Path(tmpdirpath)
        assert 2 == len(list(path.iterdir()))
        assert_equal_properties(properties1, path / "test1.properties")
        assert_equal_properties(properties2, path / "test2.properties")


def test_environment_properties_generator():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        config_generator = EMEnvironmentConfigGenerator(
            env_name="localdev", machine_name="localhost"
        )
        ad_properties = {"preferred.default.locale": "en-GB"}
        config_generator.add_properties_file("ad", ad_properties)
        tps_properties = {"tps.database.port": "1521"}
        config_generator.add_properties_file("tps", tps_properties)
        config_generator.save(tmpdirpath)

        path = Path(tmpdirpath)
        assert 2 == len(list(path.iterdir()))
        assert_equal_properties(ad_properties, path / "localdev-localhost-ad.txt")
        assert_equal_properties(tps_properties, path / "localdev-localhost-tps.txt")


env_name = "localdev"
machine_name = "localhost"

ad_properties = {
    "preferred.default.locale": "en-GB",
    "modules.list": "moduleA,moduleB",
}
tps_properties = {
    "database.user": "tps",
    "tps.modules.list": "tpsModuleA,tpsModuleB",
}


@pytest.fixture
def config_generator(capsys):
    config_generator = EMEnvironmentConfigGenerator(
        env_name=env_name, machine_name=machine_name
    )
    config_generator.add_properties_file("ad", ad_properties)
    config_generator.add_properties_file("tps", tps_properties)
    yield config_generator


def test_get_properties_from_different_components(config_generator):
    with tempfile.TemporaryDirectory() as tmpdirpath:
        config_generator.save(tmpdirpath)

        emconfig = EMEnvironmentConfig(tmpdirpath, env_name)

        assert "en-GB" == emconfig["ad"]["preferred.default.locale"]
        assert "moduleA,moduleB" == emconfig["ad"]["modules.list"]
        assert "tps" == emconfig["tps"]["database.user"]
        assert "tpsModuleA,tpsModuleB" == emconfig["tps"]["tps.modules.list"]


def test_get_properties_when_file_does_not_exist_generates_config(config_generator):
    with tempfile.TemporaryDirectory() as tmpdirpath:
        # try to get config without file existing
        config_generator.config_path = tmpdirpath
        emconfig = EMEnvironmentConfig(tmpdirpath, env_name, config_generator)

        assert "en-GB" == emconfig["ad"]["preferred.default.locale"]
        assert "moduleA,moduleB" == emconfig["ad"]["modules.list"]
        assert "tps" == emconfig["tps"]["database.user"]
