class Keynames(object):
    def __init__(self,dbfactory):
        self.dbfactory =dbfactory
    def __getitem__(self,name):
        return self.list(name)
    def list(self,keyset):
        return self.dbfactory.addb.list("SELECT KEYNAME FROM CCADMIN_IDMAP WHERE KEYSET ='"+keyset+"'")
    def load(self):
        return self

def init(app=None):
    template_API ={'_keynames'   : Keynames(app),
                  '_db'          :  app.ad_queryrunner,
                  'database'     : app.addb,
                  '_emprj'       : app.emproject
                 }
    return template_API

