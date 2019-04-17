from sql_gen.database import EMDatabase
from sql_gen.emproject import EMProject,EMConfigID
from sql_gen.database import QueryRunner,Connector
from sql_gen.config import ConfigFile
from sql_gen.utils.filesystem import ProjectLayout,Path
import sys
import os
import logging
import sql_gen
from sql_gen.log import log

PATHS= {
         "config"         : "config",
         "core_config"    : "config/core.properties",
         "ad_queries"     : "config/ad_queries.sql",
         "logging_config" : "config/logging.yaml",
         "templates"      : "templates",
         "test_templates" : "test_templates",
         "test_templates_tmp" : "test_templates/.tmp",
         "logs"           : "logs"
        }

MANDATORY_KEYS=["config",
                 "core_config",
                 "ad_queries"
                ]

class AppProject(object):
    def __init__(self,env_vars=None):
        self._config_file=None
        self._ad_query_runner=None
        self._emproject = None
        self._paths =None
        self._logger = None
        self.env_vars = env_vars

    @property
    def emproject(self):
        if not self._emproject:
            self._emproject = EMProject(env_vars=self.env_vars)
        return self._emproject

    @property
    def paths(self):
        if not self._paths:
            self._paths= ProjectLayout(self.root,PATHS,MANDATORY_KEYS)
        return self._paths

    @property
    def root(self):
        return os.path.join(self.emproject.root,"devtask")

    @property
    def ad_queryrunner(self):
        if not self._ad_query_runner:
            self._ad_query_runner = QueryRunner.make_from_app_prj(self)
        return self._ad_query_runner

    def has_root(self):
        return self.emproject.has_root()

    def product_layout(self):
        self.em_config()
        return self.emproject.product_layout()

    def em_config(self):
        if not self.emproject.default_config_id:
            self.emproject.set_default_config_id(self._emconfig_id())
        return self.emproject.config()

    @property
    def addb(self):
        emconfig = self.em_config()
        host = emconfig['database.host']
        username = emconfig['database.user']
        password = emconfig['database.pass']
        database = emconfig['database.name']
        port = emconfig['database.port']
        dbtype = emconfig['database.type']
        connector = Connector(host,
                                username,
                                password,
                                database,
                                port,
                                dbtype)
        return EMDatabase(connector)
    @property
    def config(self):
        if not self._config_file:
            self._config_file = ConfigFile(self.paths["core_config"].path)
        return self._config_file

    def _emconfig_id(self):
        #initialises project using path on
        #EM_CORE_HOME env variable
        return EMConfigID(self.config["environment.name"],
                          self.config["machine.name"],
                          self.config["container.name"])
    @staticmethod
    def set_logger(logger):
        sql_gen.log.log.set_logger(logger)

    def setup_logger(self):
        if not self._logger and self.has_root():
            if self.paths.exists('logging_config'):
                log.setup_from_file(self.paths['logging_config'].path)
            else:
                log.basic_setup(logs_dir=self.paths['logs'].path)
            self._logger = logging.getLogger("app_logger")
            print("Default logs dir is: "+self.paths['logs'].path)
        return self._logger






