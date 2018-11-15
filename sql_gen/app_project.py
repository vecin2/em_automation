from sql_gen.emproject.database import EMDatabase
from sql_gen.emproject import EMProject,EMConfigID
from sql_gen.emproject.query_runner import QueryRunner
from sql_gen.config import ConfigFile
from sql_gen.utils.filesystem import RelativePath
import sys
import os

PATHS={
        "core_config":"config/core.properties",
        "ad_queries":"config/ad_queries.sql"
        }

class AppProject(object):
    def __init__(self,emproject=EMProject()):
        self._config_file=None
        self._ad_query_runner=None
        self.emproject = emproject
        self.paths= RelativePath(self.root,PATHS)

    @property
    def root(self):
        return os.path.join(self.emproject.root,"sqltask")

    @property
    def ad_queryrunner(self):
        if not self._ad_query_runner:
            queries_path=self.paths["ad_queries"]
            self._ad_query_runner = QueryRunner.make_from_file(queries_path,
                                                               self.ad_db)
        return self._ad_query_runner

    @property
    def ad_db(self):
        emconfig = self.emproject.config(self._emconfig_id())
        host = emconfig['database.host']
        username = emconfig['database.admin.user']
        password = emconfig['database.admin.pass']
        database = emconfig['database.logical-schema']
        port = emconfig['database.port']
        dbtype = self.config['database.type']
        return EMDatabase(host,
                          username,
                          password,
                          database,
                          port,
                          dbtype)
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



