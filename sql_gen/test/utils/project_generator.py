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


class PathGenerator(object):
    def __init__(self, root):
        self.root = root
        self._files = {}
        self._folders = []

    def add_file(self, path, content=None):
        self._files[path] = content

    def remove_file(self, path):
        self._files.pop(path, None)

    def add_folder(self, folder_name):
        self._folders.append(folder_name)
        return self

    def remove_folder(self, path):
        self._folders.remove(path)

    def generate(self):
        self._generate_files()
        self._generate_folders()
        return self.root

    def _generate_files(self):
        for pathname, content in self._files.items():
            path = Path(pathname)
            (self._make_folder(path.parent) / path.name).write_text(content)

    def _generate_folders(self):
        for folder in self._folders:
            self._make_folder(folder)
        return self.root

    def _make_folder(self, folder):
        absolute_folder = self._root_path(folder)
        absolute_folder.mkdir(parents=True, exist_ok=True)
        return absolute_folder

    def _root_path(self, path):
        return self.root / path


class ProjectGenerator(PathGenerator):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self._library_generator = None
        self._project_layout = None
        self._core_properties = {}
        self._ad_properties = {}

    def with_environment_name(self, environment_name):
        self._core_properties["environment.name"] = environment_name
        return self

    def with_db_type(self, dbtype):
        return self._update_ad_properties({"database.type": dbtype})

    def _update_ad_properties(self, properties):
        self._ad_properties.update(properties)
        return self

    def with_ad_connection_details(
        self,
        host=None,
        database_name=None,
        port=None,
        user=None,
        password=None,
    ):
        db_props = {
            "database.host": host,
            "database.name": database_name,
            "database.port": port,
            "database.user": user,
            "database.pass": password,
        }
        self._ad_properties.update(db_props)
        return self

    def with_rs_connection_details(
        self,
        host=None,
        database_name=None,
        port=None,
        user=None,
        password=None,
    ):
        db_props = {
            "database.host": host,
            "database.name": database_name,
            "database.port": port,
            "database.reporting.user": user,
            "database.reporting.pass": password,
        }
        self._ad_properties.update(db_props)
        return self

    def with_tps_connection_details(
        self,
        host=None,
        database_name=None,
        port=None,
        user=None,
        password=None,
    ):
        db_props = {
            "database.host": host,
            "database.name": database_name,
            "database.port": port,
            "database.tenant-properties-service.user": user,
            "database.tenant-properties-service.pass": password,
        }
        self._ad_properties.update(db_props)
        return self

    def with_product_home(self, product_home):
        self._ad_properties["product.home"] = product_home
        return self

    def with_library_path(self, library_path):
        LIBRARY_PATH_KEY = "sqltask.library.path"
        if library_path is None:
            self._core_properties.pop(LIBRARY_PATH_KEY)
        else:
            self._core_properties[LIBRARY_PATH_KEY] = str(library_path)
        return self

    def with_library(self, library_generator):
        self._library_generator = library_generator
        self.with_library_path(library_generator.root)
        return self

    def get_library_path(self):
        return self._core_properties["sqltask.library.path"]

    @property
    def project_layout(self):
        if not self._project_layout:
            self._project_layout = ProjectLayout(self.root, PROJECT_PATHS)
        return self._project_layout

    def generate(self):
        if self._library_generator:
            self._library_generator.generate()

        self.add_file(
            "project/sqltask/config/core.properties",
            Properties(self._core_properties).to_text(),
        )

        self.env_config_generator = EMEnvironmentConfigGenerator(
            self._core_properties["environment.name"]
        )
        self.env_config_generator.add_properties_file("ad", self._ad_properties)
        self.env_config_generator.save(self.project_layout.show_config_txt)
        super().generate()
        return AppProject(emprj_path=str(self.root))


class QuickProjectGenerator(object):
    def __init__(self, root):
        self.project_generator = ProjectGenerator(root)
        self.library_generator = QuickLibraryGenerator(root.parent / "library")

    def make_project_generator(self):
        self.project_generator.add_folder("bin")
        self.project_generator.add_folder("config")
        self.project_generator.add_folder("components")
        self.project_generator.add_folder("repository")

        self.project_generator.with_environment_name("localdev")
        self.project_generator.with_db_type("oracle")
        self.project_generator.with_ad_connection_details(
            host="localhost", port="1433", user="ad", password="admin!"
        )
        self.project_generator.with_rs_connection_details(
            host="localhost", port="1433", user="rs", password="admin!"
        )
        self.project_generator.with_tps_connection_details(
            host="localhost", port="1433", user="tps", password="admin!"
        )
        self.project_generator.with_library(
            self.library_generator.make_library_generator()
        )
        return self.project_generator


class Properties(object):
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

    def __contains__(self, key):
        return key in self.config

    def put(self, property_name, property_value):
        self.config[property_name] = property_value

    def to_text(self):
        str_builder = []
        for k, v in self.config.items():
            if str_builder:
                str_builder.append("\n")
            str_builder.append(f"{k}={v}")
        return "".join(str_builder)


class LibraryGenerator(PathGenerator):

    TEMPLATES_PATH = Path("templates")

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self._ad_queries = None
        self._templates = []

    def add_template(self, filename, content):
        self.add_file(self._template_path(filename), content)
        return self

    def _template_path(self, filename):
        return self.TEMPLATES_PATH / filename

    def with_ad_queries(self, file_content):
        self._ad_queries = Properties(file_content)
        return self

    def append_template(self, filename, content):
        self._templates["filename"] = content

    def generate(self):
        library = SQLTaskLib(self.root)
        if self._ad_queries:
            filepath = library.db_queries("ad")
            self.add_file(filepath, self._ad_queries.to_text())
        super().generate()
        return library


class QuickLibraryGenerator(object):
    def __init__(self, root):
        self.library_generator = LibraryGenerator(root)

    def make_library_generator(self):
        self.library_generator.add_folder("templates")
        return self.library_generator