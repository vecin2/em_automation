from sql_gen.config import ConfigFile
class AttrDict(object):
    def __init__(self,dict):
        self.dict = dict
    def __getattr__(self, item):
        return self.dict[item]

    def __dir__(self):
        return super().__dir__() + [str(k) for k in self.keys()]

class CallableList(object):
    def __init__(self,string,emdb):
       self.string = string
       self.emdb = emdb

    def __call__(self,*args):
        formatted_query = self.string.format(*args)
        return self.emdb.list(formatted_query)

class CallableFind(object):
    def __init__(self,string,emdb):
       self.string = string
       self.emdb = emdb

    def __call__(self,*args):
        formatted_query = self.string.format(*args)
        return self.emdb.find(formatted_query)

class List(AttrDict):
    def __init__(self,query_dict,emdb):
        super().__init__(query_dict)
        self.emdb =emdb
    def __getattr__(self, item):
        return CallableList(super().__getattr__(item),self.emdb)

class Find(AttrDict):
    def __init__(self,query_dict,emdb):
        super().__init__(query_dict)
        self.emdb =emdb
    def __getattr__(self, item):
        return CallableFind(super().__getattr__(item),self.emdb)

class QueryRunner(object):
    def __init__(self,query_dict, emdb):
        self.query_dict = query_dict
        self.emdb = emdb
        self.list = List(self.query_dict,self.emdb)
        self.find = Find(self.query_dict,self.emdb)

    def has_query(self,key):
        return key in self.query_dict

    @staticmethod
    def make_from_file(file_path,emdb):
        config_file=ConfigFile(file_path)
        return QueryRunner(config_file.properties, emdb)


