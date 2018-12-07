from sql_gen.database import EMDatabase
from sql_gen.emproject import EMProject,EMConfigID
from sql_gen.database import QueryRunner,Connector
from sql_gen.config import ConfigFile
from sql_gen.utils.filesystem import RelativePath
import sys
import os
import logging

PATHS={
        "config": "config",
        "core_config":"config/core.properties",
        "ad_queries":"config/ad_queries.sql"
        }

class AppProject(object):
    def __init__(self,emproject=EMProject()):
        self._config_file=None
        self._ad_query_runner=None
        self.emproject = emproject
        self.paths= RelativePath(self.root,PATHS)
        self._logger = None

    @property
    def root(self):
        return os.path.join(self.emproject.root,"sqltask")

    @property
    def logger(self):
        return self.get_logger()

    @property
    def ad_queryrunner(self):
        if not self._ad_query_runner:
            queries_path=self.paths["ad_queries"]
            self._ad_query_runner = QueryRunner.make_from_file(queries_path,
                                                               self.addb)
        return self._ad_query_runner

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
            self._config_file = ConfigFile(self.paths["core_config"])
        return self._config_file

    def _emconfig_id(self):
        #initialises project using path on
        #EM_CORE_HOME env variable
        return EMConfigID(self.config["environment.name"],
                          self.config["machine.name"],
                          self.config["container.name"])

    def get_logger(self):
        if not self._logger:
            self._logger = logging.getLogger("app_logger")
        return self._logger





