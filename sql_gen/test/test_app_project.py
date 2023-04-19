import os
import tempfile
from pathlib import Path

from st_librarian.sqltasklib import SQLTaskLib

from sql_gen.app_project import AppProject
from sql_gen.test.emproject.utils import EMEnvironmentConfigGenerator

# from sql_gen.emproject import EMProject

PROJECT_PATHS = {
    "core_config": "project/sqltask/config/core.properties",
    "show_config_txt": "work/config/show-config-txt",
}


class ProjectLayout(object):
    def __init__(self, root, paths):
        self.paths = paths
        if str(root):
            root = Path(root)
        self.root = root

    def __getattr__(self, attr):  # self[]
        if attr in self.paths:
            return self.get_absolute_path(attr)
        else:
            raise AttributeError(attr)

    def get_absolute_path(self, key):
        return self.root / self.paths[key]

    def write_text(self, key, content):
        self.get_absolute_path(key).parent.mkdir(parents=True, exist_ok=True)
        self.get_absolute_path(key).write_text(content)


class ProjectGenerator(object):
    def __init__(self, root):
        self.root = root
        self.core_properties_generator = None
        self.library = None
        self._project_layout = None
        self._core_properties = {}
        self._ad_properties = {}

    def with_environment_name(self, environment_name):
        self._core_properties["environment.name"] = environment_name
        return self

    def with_ad_connection_details(
        self,
        database_type=None,
        host=None,
        database_name=None,
        port=None,
        user=None,
        password=None,
    ):
        db_props = {
            "database.type": database_type,
            "database.host": host,
            "database.name": database_name,
            "database.port": port,
            "database.user": user,
            "database.pass": password,
        }
        self._ad_properties.update(db_props)
        return self

    # def _with_core_config(self, file_content):
    #     self._core_properties = Properties(file_content)
    #     self.core_properties_generator = PropertiesFileGenerator(file_content)
    #     return self

    def with_library(self, library):
        self._core_properties["sqltask.library.path"] = str(library.rootpath)
        self.library = library
        return self

    @property
    def project_layout(self):
        if not self._project_layout:
            self._project_layout = ProjectLayout(self.root, PROJECT_PATHS)
        return self._project_layout

    def generate(self):
        self.project_layout.write_text(
            "core_config", Properties(self._core_properties).to_text()
        )

        self.env_config_generator = EMEnvironmentConfigGenerator(
            self._core_properties["environment.name"]
        )
        self.env_config_generator.add_properties_file("ad", self._ad_properties)
        self.env_config_generator.save(self.project_layout.show_config_txt)
        return AppProject(emprj_path=str(self.root))


class Properties(dict):
    def __init__(self, properties):
        if type(properties) == str:
            properties = self._to_dict(properties)
        self.config = properties

    def __getitem__(self, name):
        return self.config[name]

    def __setitem__(self, name, value):
        self.config[name] = value

    def _to_dict(self, config_content):
        dict = {}
        for line in config_content.splitlines():
            segments = line.split("=")
            k = segments[0]
            v = "=".join(segments[1:])  # e.g property=some property with = within value
            dict[k] = v
        return dict

    def put(self, property_name, property_value):
        self.config[property_name] = property_value

    def to_text(self):
        str_builder = []
        for k, v in self.config.items():
            if str_builder:
                str_builder.append("\n")
            str_builder.append(f"{k}={v}")
        return "".join(str_builder)


class LibraryGenerator(object):
    def __init__(self, root):
        self.root = root
        self._ad_queries = None

    def with_ad_queries(self, file_content):
        self._ad_queries = Properties(file_content)
        return self

    def generate(self):
        library = SQLTaskLib(self.root)
        filepath = library.db_queries("ad")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(self._ad_queries.to_text())
        return library
        # self.library_layout.write_text("core_config", self._core_properties.to_text())


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


def test_instantiate_ad_queryrunner():
    query_name = "v_names__by_ed"
    query_content = "SELECT * FROM verb_name WHERE NAME='{}'"
    queries_content = f"{query_name}={query_content}"
    with tempfile.TemporaryDirectory() as root:
        root_path = Path(root)
        project_generator = ProjectGenerator(root_path / "trunk")
        library_generator = LibraryGenerator(root_path / "library").with_ad_queries(
            queries_content
        )
        project_generator.with_environment_name("localdev")
        project_generator.with_library(library_generator.generate())
        project_generator.with_ad_connection_details(
            host="localhost", port="1433", user="sa", password="admin!"
        )
        project = project_generator.generate()
        assert project.ad_queryrunner.has_query("v_names__by_ed")
        assert query_content == project.ad_queryrunner.query_dict["v_names__by_ed"]
