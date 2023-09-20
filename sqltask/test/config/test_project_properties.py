import tempfile
from pathlib import Path

from sqltask.emproject.config import ProjectProperties
from sqltask.test.config.utils import (PropertiesFileGenerator,
                                       PropertiesFolderGenerator,
                                       assert_equal_properties)
from sqltask.test.emproject.utils import EMEnvironmentConfigGenerator


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


def make_core_properties(properties_dict, filepath):
    PropertiesFileGenerator(properties_dict).save(filepath)


def make_environment_config(folderpath, *components_props):
    config_generator = EMEnvironmentConfigGenerator(
        env_name="localdev", machine_name="localhost"
    )
    for component_props in components_props:
        config_generator.add_properties_file(component_props[0], component_props[1])

    config_generator.save(folderpath)


def make_project_properties(project_root):
    core_properties = {"environment.name": "localdev"}

    ad_properties = {"preferred.default.locale": "en-GB"}
    tps_properties = {"tps.database.port": "1521"}

    project_props = ProjectProperties(project_root)
    make_core_properties(core_properties, project_props.core_properties_path)
    make_environment_config(
        project_props.environment_properties_path,
        ("ad", ad_properties),
        ("tps", tps_properties),
    )
    return project_props


def test_get_core_and_emenvironment_properties():
    with tempfile.TemporaryDirectory() as project_root:
        project_props = make_project_properties(project_root)

        assert "localdev" == project_props.core["environment.name"]
        assert "en-GB" == project_props.em["preferred.default.locale"]
        assert "en-GB" == project_props.em.preferred_default_locale
        assert "1521" == project_props.em.tps_database_port


def test_get_library_path():
    with tempfile.TemporaryDirectory() as project_root:
        project_props = ProjectProperties(project_root)
        project_props.library_file_path.parent.mkdir(parents=True)
        project_props.library_file_path.write_text("/mnt/c/em/sqltask-library")

        assert "/mnt/c/em/sqltask-library" == str(project_props.library_path)
