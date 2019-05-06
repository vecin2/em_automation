import yaml

import sql_gen
from sql_gen.database.query_runner import QueryDict
from sql_gen.config import ConfigFile
from sql_gen.app_project import AppProject

class Keynames(object):
    def __init__(self,dbfactory):
        self.dbfactory =dbfactory
    def __getitem__(self,name):
        return self.list(name)
    def __getattr__(self,name):
        if name.startswith("FULL_"):
            name = name.replace("FULL_","")
            prefix ="@"+name+"."
            keynames = self.list(name)
            result = [prefix+keyname for keyname in keynames]
            result.append("NULL")
            return result
        else:
            return self.list(name)

    def list(self,keyset):
        return self.dbfactory.addb.list("SELECT KEYNAME FROM CCADMIN_IDMAP WHERE KEYSET ='"+keyset+"'")
    def load(self):
        return self

def init(app=None,emprj_path=None):
    if emprj_path:
        app = AppProject.make(emprj_path)
    template_API ={'_keynames'   : Keynames(app),
                  '_db'          :  app.ad_queryrunner,
                  '_database'    : app.addb,
                  '_Query'       : QueryDict(ConfigFile(app.paths["ad_queries"].path).properties),
                  '_emprj'       : app.emproject
                 }
    template_API.update(context_values(app.paths['context_values'].path))
    return template_API

def context_values(filepath):
    try:
        with open(filepath, 'r') as stream:
            yaml_dict = yaml.safe_load(stream)
            return yaml_dict
    except FileNotFoundError as exc:
        sql_gen.logger.warning("No context values are added, context config file '"+filepath+"' does not exist")
        return {}
    except yaml.YAMLError as exc:
        sql_gen.logger.warning("No context values are added, context config file '"+filepath+"' does not exist")

