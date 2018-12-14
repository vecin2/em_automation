class Keynames(object):
    def __init__(self,app):
        self.app =app
    def __getitem__(self,name):
        return self.list(name)
    def list(self,keyset):
        return self.app.addb.list("SELECT KEYNAME FROM CCADMIN_IDMAP WHERE KEYSET ='"+keyset+"'")

def init(app=None):
    return{'_keynames':Keynames(app),
                  '_addb'    :app.ad_queryrunner,
                  '_emprj'   :app.emproject
                 }
