from sql_gen.database.query_runner import QueryDict
from sql_gen.config import ConfigFile
from sql_gen.app_project import AppProject

class Keynames(object):
    def __init__(self,dbfactory):
        self.dbfactory =dbfactory
    def __getitem__(self,name):
        return self.list(name)
    def list(self,keyset):
        return self.dbfactory.addb.list("SELECT KEYNAME FROM CCADMIN_IDMAP WHERE KEYSET ='"+keyset+"'")
    def load(self):
        return self

def init(app=None,path=None):
    if path:
        app = AppProject.make(path=path)
    template_API ={'_keynames'   : Keynames(app),
                  '_db'          :  app.ad_queryrunner,
                  '_database'    : app.addb,
                  '_Query'       : QueryDict(ConfigFile(app.paths["ad_queries"].path).properties),
                  '_emprj'       : app.emproject
                 }
    return template_API

