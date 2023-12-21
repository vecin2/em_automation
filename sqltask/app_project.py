import logging
from pathlib import Path

from st_librarian.sqltasklib import SQLTaskLib

import sqltask
from sqltask.database import Connector, DBSchema, Database, QueryRunner
from sqltask.emproject.ccadmin import CCAdmin
from sqltask.emproject.config import ProjectProperties
from sqltask.log import log
from sqltask.utils.filesystem import ProjectLayout

PATHS = {
    "config": "project/sqltask/config",
    "core_config": "project/sqltask/config/core.properties",
    "local_config": "project/sqltask/config/local.properties",
    "logging_config": "project/sqltask/config/logging.yaml",
    "logs": "project/sqltask/logs",
    "ccadmin": "bin",
    "db_releases_file": "config/releases.xml",
    "sql_modules": "modules",
    "repo_modules": "repository/default",
    "show_config_txt": "work/config/show-config-txt",
}

MANDATORY_KEYS = ["config", "core_config"]


class AppProject(object):
    def __init__(self, emprj_path=None):
        self._config_file = None
        self._em_config = None
        self._ad_query_runner = None
        self._rs_query_runner = None
        self._tps_query_runner = None
        self._emproject = None
        self._paths = None
        self._logger = None
        self.emprj_path = emprj_path
        self._addb = None
        self._rsdb = None
        self._tpsdb = None
        self._library = None
        self._em_config = None
        self._project_properties = None
        self._ccadmin_client = None
        self._library_path = None
        self._db = None
        self._merged_config = None

    def make(emprj_path=None):
        return AppProject(emprj_path=emprj_path)

    @property
    def emroot(self):
        return Path(self.emprj_path)

    @property
    def paths(self):
        if not self._paths:
            self._paths = ProjectLayout(self.emroot, PATHS, MANDATORY_KEYS)
        return self._paths

    @property
    def ad_queryrunner(self):
        if not self._ad_query_runner:
            self._ad_query_runner = QueryRunner.make_from_file(
                self.library().db_queries("ad"),
                self.addb,
            )
        return self._ad_query_runner

    @property
    def rs_queryrunner(self):
        if not self._rs_query_runner:
            self._rs_query_runner = QueryRunner.make_from_file(
                self.library().db_queries("rs"),
                self.rsdb,
            )
        return self._rs_query_runner

    @property
    def tps_queryrunner(self):
        if not self._tps_query_runner:
            self._tps_query_runner = QueryRunner.make_from_file(
                self.library().db_queries("tps"),
                self.tpsdb,
            )
        return self._tps_query_runner

    def product_layout(self):
        return ProjectLayout(self.em_config()["product.home"], PATHS)

    def em_config(self):
        return self.project_properties.em
    
    def merged_config(self):
        if not self._merged_config:
            self._merged_config = self.project_properties.merged_config
        return self._merged_config

    @property
    def ccadmin_client(self):
        if not self._ccadmin_client:
            self._ccadmin_client = CCAdmin(self.emroot / "bin")

        return self._ccadmin_client

    @property
    def project_properties(self):
        if not self._project_properties:
            self._project_properties = ProjectProperties(
                self.emroot, config_generator=self.ccadmin_client
            )
        return self._project_properties

    def get_schema(self, schema_name):
        if schema_name == "tenant_properties_service":
            return self.tpsdb
        else:
            return self.addb

    @property
    def db(self):
        if not self._db:
            self._db = Database(self.em_config())
        return self._db

    @property
    def addb(self):
        return self.db.addb

    @property
    def tpsdb(self):
        return self.db.tpsdb

    @property
    def rsdb(self):
        return self.db.rsdb

    @property
    def config(self):
        return self.project_properties.core

    def _get_database(
        self,
        host=None,
        user=None,
        password=None,
        dbname=None,
        port=None,
        dbtype=None,
        sqlserver_driver_name=None,
        sqlserver_conn_str_name=None,
        component_name="ad",
    ):
        emconfig = self.em_config()
        host = emconfig[host]
        username = emconfig[user]
        password = emconfig[password]
        database = emconfig[dbname]
        port = emconfig[port]
        dbtype = emconfig[dbtype]
        sqlserver_driver = ""
        sqlserver_conn_str = ""
        if dbtype == "sqlServer":
            if sqlserver_conn_str_name in emconfig:
                sqlserver_conn_str = emconfig[sqlserver_conn_str_name]
            else:
                sqlserver_driver = emconfig[sqlserver_driver_name]
        connector = Connector(
            host,
            username,
            password,
            database,
            port,
            dbtype,
            sqlserver_driver,
            sqlserver_conn_str,
        )
        return DBSchema(connector)

    @staticmethod
    def set_logger(logger):
        sqltask.log.log.set_logger(logger)

    def setup_logger(self):
        if not self._logger:
            if self.paths.exists("logging_config"):
                log.setup_from_file(str(self.paths["logging_config"]))
            else:
                log.basic_setup(logs_dir=str(self.paths["logs"]))
            self._logger = logging.getLogger("app_logger")
        return self._logger

    def logging_config_file(self):
        logger_config_path = self.paths["logging_config"]
        if logger_config_path.exists():
            return logger_config_path
        return None

    def sqltask_logs_dir(self):
        return str(self.paths["logs"])

    def get_db_release_version(self):
        db_release_version = self._get_db_release_version_from_properties()
        if db_release_version:
            return db_release_version
        return self._get_db_release_version_from_file()

    def _get_db_release_version_from_properties(self):
        if "db.release.version" in self.config:
            return self.config["db.release.version"]
        return ""

    def _get_db_release_version_from_file(self):
        latest_release = ""
        # Get value from last line of releases.xml
        # Example release.xml line:
        # <release value="APSU_DHL22_03" after="APSU_DHL22_02"/>
        reversed_lines = reversed(
            self.paths["db_releases_file"].read_text().splitlines()
        )
        for line in reversed_lines:
            splitted_value = line.split('value="')
            if len(splitted_value) > 1:
                latest_release = splitted_value[1].split('"')[0]
                break

        return latest_release

    def library_path(self):
        if not self._library_path:
            self._library_path = self.compute_library_path()
        return self._library_path

    def set_library_path(self, library_path):
        self._library_path = library_path

    def compute_library_path(self):
        try:
            return self.project_properties.library_path
        except Exception:
            error_msg = """Library path not set for current project. Create a .library file under {}/project/sqltask/config, where the content of the file is the path to a sqltask library, e.g c:\\em\\sqltask_library""".format(
                str(self.emroot)
            )
            raise ValueError(error_msg)

    def library(self):
        if not self._library:
            library_path = self.library_path()
            if library_path.exists():
                self._library = SQLTaskLib(library_path)
            else:
                error_msg = f"'.library' points to an invalid path '{self.library_path()}'.\nPlease edit '.library' file and make sure it points to the parent folder of your 'templates' folder."
                raise ValueError(error_msg)
        return self._library
