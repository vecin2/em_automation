import os
import tempfile
from pathlib import Path

import pytest

from sql_gen.emproject.config import EMEnvironmentConfig
from sql_gen.test.config.utils import assert_equal_properties
from sql_gen.test.emproject.utils import EMEnvironmentConfigGenerator


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
test_tps_properties = {
    "database.user": "test_tps",
    "tps.modules.list": "test_tpsModuleA,test_tpsModuleB",
}


@pytest.fixture
def localdev_generator(capsys):
    localdev_generator = EMEnvironmentConfigGenerator(
        env_name="localdev", machine_name="localhost"
    )
    localdev_generator.add_properties_file("ad", ad_properties)
    localdev_generator.add_properties_file("tps", tps_properties)
    yield localdev_generator


@pytest.fixture
def test_generator(capsys):
    test_generator = EMEnvironmentConfigGenerator(
        env_name="test", machine_name="localhost"
    )
    test_generator.add_properties_file("ad", ad_properties)
    test_generator.add_properties_file("tps", test_tps_properties)
    yield test_generator


def test_get_properties_from_different_components(localdev_generator, test_generator):
    with tempfile.TemporaryDirectory() as tmpdirpath:
        localdev_generator.save(tmpdirpath)
        test_generator.save(tmpdirpath)

        emconfig = EMEnvironmentConfig(tmpdirpath, env_name)

        assert "en-GB" == emconfig.preferred_default_locale
        assert "moduleA,moduleB" == emconfig.modules_list

        assert "tps" == emconfig.database_user
        assert "tpsModuleA,tpsModuleB" == emconfig.tps_modules_list


def test_ignore_property_files_with_failed_interpolation(localdev_generator):
    # sometimes property fails do not resolve all the vars, ignore those
    with tempfile.TemporaryDirectory() as tmpdirpath:
        invalid_properties = {"database.pass": "${database.user}"}

        localdev_generator.add_properties_file("km-bookmark-service", invalid_properties)
        localdev_generator.save(tmpdirpath)

        emconfig = EMEnvironmentConfig(tmpdirpath, env_name)

        assert "en-GB" == emconfig.preferred_default_locale
        assert "moduleA,moduleB" == emconfig.modules_list

        assert "tps" == emconfig.database_user
        assert "tpsModuleA,tpsModuleB" == emconfig.tps_modules_list


def test_get_properties_when_file_does_not_exist_generates_config(localdev_generator):
    with tempfile.TemporaryDirectory() as tmpdirpath:
        # set config_path so fake ccadmin generator knows where to create files
        config_path = tmpdirpath + os.sep + "test"
        localdev_generator.config_path = config_path

        emconfig = EMEnvironmentConfig(config_path, env_name, localdev_generator)

        assert "en-GB" == emconfig["preferred.default.locale"]
        assert "moduleA,moduleB" == emconfig["modules.list"]
        assert "tps" == emconfig["database.user"]
