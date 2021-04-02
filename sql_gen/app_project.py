import sql_gen
from sql_gen.database import EMDatabase
from sql_gen.emproject import EMProject, EMConfigID, emproject_home
from sql_gen.database import QueryRunner, Connector
from sql_gen.config import ConfigFile
from sql_gen.utils.filesystem import ProjectLayout, Path
import sys
import os
import logging
import sql_gen
from sql_gen.log import log

PATHS = {
    "config": "config",
    "core_config": "config/core.properties",
    "ad_queries": "config/ad_queries.sql",
    "rs_queries": "config/rs_queries.sql",
    "context_values": "config/context_values.yaml",
    "test_context_values": "config/test_context_values.yaml",
    "logging_config": "config/logging.yaml",
    "templates": "templates",
    "test_templates": "test_templates",
    "test_templates_tmp": "test_templates/.tmp",
    "logs": "logs",
}

MANDATORY_KEYS = ["config", "core_config", "ad_queries"]


class AppProject(object):
    def __init__(self, env_vars=None, emprj_path=None):
        self._config_file = None
        self._em_config = None
        self._ad_query_runner = None
        self._rs_query_runner = None
        self._emproject = None
        self._paths = None
        self._logger = None
        self.env_vars = env_vars
        self.emprj_path = emprj_path
        self._addb = None
        self._rsdb = None

    def make(emprj_path=None):
        return AppProject(emprj_path=emprj_path)

    @property
    def emproject(self):
        if not self._emproject:
            self._emproject = EMProject(
                env_vars=self.env_vars, emprj_path=self.emprj_path
            )
        return self._emproject

    @property
    def paths(self):
        if not self._paths:
            self._paths = ProjectLayout(self.root, PATHS, MANDATORY_KEYS)
        return self._paths

    @property
    def root(self):
        emprj_home = self.emproject.root
        destask_filepath = os.path.join(emprj_home, sql_gen.appname)
        if os.path.isfile(destask_filepath):
            with open(destask_filepath) as f:
                devtaskpath = f.readline().strip()
        else:
            devtaskpath = os.path.join("project", sql_gen.appname)
        return os.path.join(self.emproject.root, devtaskpath)

    @property
    def ad_queryrunner(self):
        if not self._ad_query_runner:
            self._ad_query_runner = QueryRunner.make_from_file(
                self.paths["ad_queries"].path, self.addb
            )
        return self._ad_query_runner

    @property
    def rs_queryrunner(self):
        if not self._rs_query_runner:
            self._rs_query_runner = QueryRunner.make_from_file(
                self.paths["rs_queries"].path, self.rsdb
            )
        return self._rs_query_runner

    def has_root(self):
        return self.emproject.has_root()

    def product_layout(self):
        self.em_config()
        return self.emproject.product_layout()

    def em_config(self):
        if not self._em_config:
            if not self.emproject.default_config_id:
                self.emproject.set_default_config_id(self._emconfig_id())
            self._em_config = self.emproject.config()
        return self._em_config

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
            )
        return self._addb

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
            )
        return self._rsdb

    @property
    def config(self):
        if not self._config_file:
            self._config_file = ConfigFile(self.paths["core_config"].path)
        return self._config_file

    def _get_database(
        self, host=None, user=None, password=None, dbname=None, port=None, dbtype=None
    ):
        emconfig = self.em_config()
        host = emconfig[host]
        username = emconfig[user]
        password = emconfig[password]
        database = emconfig[dbname]
        port = emconfig[port]
        dbtype = emconfig[dbtype]
        connector = Connector(host, username, password, database, port, dbtype)
        return EMDatabase(connector)

    def _emconfig_id(self):
        # initialises project using path on
        # EM_CORE_HOME env variable
        return EMConfigID(
            self.config["environment.name"],
            self.config["machine.name"],
            self.config["container.name"],
        )

    @staticmethod
    def set_logger(logger):
        sql_gen.log.log.set_logger(logger)

    def setup_logger(self):
        if not self._logger and self.has_root():
            if self.paths.exists("logging_config"):
                log.setup_from_file(self.paths["logging_config"].path)
            else:
                log.basic_setup(logs_dir=self.paths["logs"].path)
            self._logger = logging.getLogger("app_logger")
            print("Default logs dir is: " + self.paths["logs"].path)
        return self._logger
