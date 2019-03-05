from sql_gen.config import ConfigFile
import re
import string
from fuzzyfinder import fuzzyfinder


class AttrDict(object):
    def __init__(self,dict):
        self.dict = dict
    def __getattr__(self, item):
        if item not in self.dict:
            assert False, self._no_query_found_error(item)
        return self.dict[item]

    def _no_query_found_error(self, item):
        suggestions = list(fuzzyfinder(item, self.dict.keys()))
        no_query_defined="No query defined called '"+item+"'."
        if not suggestions:
            return no_query_defined
        else:
            return no_query_defined+" Did you mean?\n"+ "\n".join(suggestions)


    def __dir__(self):
        return super().__dir__() + [str(k) for k in self.keys()]

class CallableDBQuery(object):
    def __init__(self,op_name,key,string,emdb):
       self.string = string
       self.key = key
       self.emdb = emdb
       self.op_name=op_name

    def __call__(self,*args,**kwargs):
        args_expected=self.count_placeholders(self.string)
        args_given=len(args)+len(kwargs)

        error_msg= "Method '"+self.key+"' takes "+str(args_expected)+ " params ("+ str(args_given)+" given)"
        assert args_expected==args_given, error_msg
        formatted_query = self.string.format(*args,**kwargs)

        function = getattr(self.emdb,self.op_name)
        return function(formatted_query)

    def count_placeholders(self,fmt):
        count = 0
        L = string.Formatter().parse(fmt)
        for x in L:
            if x[1] is not None:
                count += 1
        return count

class DBOperation(AttrDict):
    def __init__(self,op_name,query_dict,emdb_loader):
        super().__init__(query_dict)
        self.emdb_loader =emdb_loader
        self.op_name=op_name
        self._emdb =None
    def __getattr__(self, item):
        return CallableDBQuery(self.op_name,item,super().__getattr__(item),self.emdb)

    @property
    def emdb(self):
        if not self._emdb:
            self._emdb = self.emdb_loader.addb
        return self._emdb

class QueryRunner(object):
    def __init__(self,query_dict, emdb,app_project=None):
        self._query_dict = None
        self._emdb = None
        self._app_project =app_project
        self.find = DBOperation("find",self.query_dict,app_project)
        self.list = DBOperation("list",self.query_dict,app_project)
        self._query_dict=None
        self._list=None

    @property
    def emdb(self):
        if not self._emdb:
            self._emdb=self.app_project.addb
        return self._emdb
    @property
    def query_dict(self):
        if not self._query_dict:
            queries_path=self._app_project.paths["ad_queries"].path
            config_file=ConfigFile(queries_path)
            self._query_dict= config_file.properties
        return self._query_dict
    def has_query(self,key):
        return key in self.query_dict

    @staticmethod
    def make_from_app_prj(app_project):
        return QueryRunner(None,None,app_project =app_project)

