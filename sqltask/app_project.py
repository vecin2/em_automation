import logging
from pathlib import Path

from st_librarian.sqltasklib import SQLTaskLib

import sqltask
from sqltask.database import Connector, EMDatabase, QueryRunner
from sqltask.emproject.ccadmin import CCAdmin
from sqltask.emproject.config import ProjectProperties
from sqltask.log import log
from sqltask.utils.filesystem import ProjectLayout

PATHS = {
    "config": "project/sqltask/config",
    "core_config": "project/sqltask/config/core.properties",
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

    def make(emprj_path=None):
        return AppProject(emprj_path=emprj_path)

    @property
    def emroot(self):
        return Path(self.emprj_path)
        return self.emproject.root

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
    def addb(self):
        if not self._addb:
            self._addb = self._get_database(
                host="database.host",
                user="database.user",
                password="database.pass",
                dbname="database.name",
                port="database.port",
                dbtype="database.type",
                sqlserver_driver_name="sqlServer.driver",
                sqlserver_conn_str_name="sqlServer.conn.str",
            )
        return self._addb

    @property
    def tpsdb(self):
        if not self._tpsdb:
            self._tpsdb = self._get_database(
                host="database.host",
                user="database.tenant-properties-service.user",
                password="database.tenant-properties-service.pass",
                dbname="database.name",
                port="database.port",
                dbtype="database.type",
                sqlserver_driver_name="sqlServer.driver",
                sqlserver_conn_str_name="sqlServer.conn.str",
                component_name="tenant-properties-service",
            )
        return self._tpsdb

    @property
    def rsdb(self):
        if not self._rsdb:
            self._rsdb = self._get_database(
                host="database.host",
                user="database.reporting.user",
                password="database.reporting.pass",
                dbname="database.name",
                port="database.port",
                dbtype="database.type",
                sqlserver_driver_name="sqlServer.driver",
                sqlserver_conn_str_name="sqlServer.conn.str",
            )
        return self._rsdb

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
        return EMDatabase(connector)

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
            print("Default logs dir is: " + str(self.paths["logs"]))
        return self._logger

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

    def task_library_path(self):
        return self.config["sqltask.library.path"]

    def library(self):
        if not self._library:
            self._library = SQLTaskLib(Path(self.task_library_path()))
        return self._library
