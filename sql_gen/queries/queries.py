from sql_gen.current_project import app

addb =app.ad_db
class Keynames(object):
    @property
    def ED(self):
        return self.list("ED")
    def list(self,keyset):
        return addb.list("SELECT KEYNAME FROM CCADMIN_IDMAP WHERE KEYSET ='"+keyset+"'")

class EntityDefinition(object):
    @property
    def verb_names(self):
        query="SELECT V.NAME FROM EVA_VERB V,CCADMIN_IDMAP IDMAP where IDMAP.ID = V.ENTITY_DEF_ID and IDMAP.KEYSET ='ED' and IDMAP.KEYNAME = '"+self.keyname+"'"
        return addb.list(query)

    def with_keyname(self,keyname):
        self.keyname=keyname
        return self

class ProcessDescriptor(object):

    def load(self,entity_keyname,verb_name):
        self.entity_keyname = entity_keyname
        query="SELECT * FROM EVA_VERB V, EVA_PROCESS_DESCRIPTOR PD, EVA_PROCESS_DESC_REFERENCE PDR, CCADMIN_IDMAP IDMAP WHERE V.PROCESS_DESC_REF_ID = PDR.ID AND PDR.PROCESS_DESCRIPTOR_ID = PD.ID AND IDMAP.ID = V.ENTITY_DEF_ID and IDMAP.KEYSET ='ED' AND V.NAME ='"+verb_name+"' and IDMAP.KEYNAME = '"+entity_keyname+"'"
        self.verb_name = verb_name
        return addb.query(query)[0]
