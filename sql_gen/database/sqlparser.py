import re
import sqlparse

storage_table = {
                 "CC": {"Home": 100},
                 "ENV":{"Dflt": 666},
                 "RELEASE":{"ID":1},
                 "ET":{"Agent":602}
                }

class RelativeIdLoader(object):
    def __init__(self,storage_table=storage_table):
        self.storage_table =storage_table
    def load(self,keyset,keyname):
        return self.storage_table[keyset][keyname]

class RelativeId(object):
    relativeid_exp="(?<=[^\w])@\w*\.\w*"
    def __init__(self,string,loader=None):
        self.string = string
        self.loader =loader

    @property
    def keyset(self):
        return self.string.split(".")[0][1:]

    @property
    def keyname(self):
        return self.string.split(".")[1]

    def real_id(self):
        return str(self.loader.load(self.keyset,self.keyname))

    def replace_all_instances(self,sqltext):
        return sqltext.replace(self.string,self.real_id())


class RelativeIdReplacer(object):
    def __init__(self,loader=None):
        self.loader = loader
    REG_EXP="(?<=[^\w])@\w*\.\w*"
    def find_all(self,sqltext):
        ids =re.findall(self.REG_EXP,sqltext)
        #remove duplicates
        return list(set(ids))

    def replace(self,sqltext):
        relative_ids = self.find_all(sqltext)
        for str_relative_id in relative_ids:
            relative_id = RelativeId(str_relative_id,loader=self.loader)
            sqltext = relative_id.replace_all_instances(sqltext)
        return sqltext

class SQLParser(object):
    def __init__(self,loader=RelativeIdLoader()):
        self.relativeId_replacer = RelativeIdReplacer(loader)

    def strip_comments(self,sqltext):
        return sqlparse.format(sqltext,strip_comments=True).strip()

    def split(self,sqltext):
        result =[]
        for statement in sqlparse.split(sqltext):
            #remove semicolon - otherwise throws exc when run
            if statement and statement[-1:]==";":
                statement = statement[:-1]
            result.append(statement)
        return result

    def parse_runnable_statements(self,sqltext):
        sqltext = self.relativeId_replacer.replace(sqltext)
        sqltext = self.strip_comments(sqltext)
        return self.split(sqltext)

