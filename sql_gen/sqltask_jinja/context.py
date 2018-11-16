from sql_gen import app


class Keynames(object):
    def __getitem__(self,name):
        return self.list(name)
    def list(self,keyset):
        return app.addb.list("SELECT KEYNAME FROM CCADMIN_IDMAP WHERE KEYSET ='"+keyset+"'")

initial_context={'_keynames':Keynames(),
                  '_addb'    :app.ad_queryrunner
                 }
