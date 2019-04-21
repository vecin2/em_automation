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

class CallableFormatString(object):
    def __init__(self,key,string):
       self.key =key
       self.string = string

    def __call__(self,*args,**kwargs):
        return self.format_string(*args,**kwargs)

    def format_string(self,*args,**kwargs):
        args_expected=self.count_placeholders(self.string)
        args_given=len(args)+len(kwargs)

        error_msg= "Method '"+self.key+"' takes "+str(args_expected)+ " params ("+ str(args_given)+" given)"
        assert args_expected==args_given, error_msg
        return self.string.format(*args,**kwargs)

    def count_placeholders(self,fmt):
        count = 0
        L = string.Formatter().parse(fmt)
        for x in L:
            if x[1] is not None:
                count += 1
        return count

class CallableDBQuery(CallableFormatString):
    def __init__(self,op_name,key,string,emdb):
       super().__init__(key,string)
       self.emdb = emdb
       self.op_name=op_name

    def __call__(self,*args,**kwargs):
        formatted_query = super().__call__(*args,**kwargs)
        function = getattr(self.emdb,self.op_name)
        return function(formatted_query)


class QueryDict(AttrDict):
    def __init__(self,query_dict):
        super().__init__(query_dict)

    @staticmethod
    def get_instance():
        """"""


    def __getattr__(self, item):
        return CallableFormatString(item,super().__getattr__(item))

class DBOperation(AttrDict):
    def __init__(self,op_name,query_dict,emdb_loader):
        super().__init__(query_dict)
        self.emdb_loader =emdb_loader
        self.op_name=op_name
        self.addb =None
        if emdb_loader:
            self.addb =emdb_loader.addb

    def __getattr__(self, item):
        return CallableDBQuery(self.op_name,item,super().__getattr__(item),self.addb)


class QueryRunner(object):
    def __init__(self,query_dict=None, emdb=None,app_project=None,filepath=None):
        self._filepath =filepath
        self._query_dict = query_dict
        self._addb = emdb
        self._app_project =app_project
        self.find = DBOperation("find",self.query_dict,self)
        self.list = DBOperation("list",self.query_dict,self)
        self.fetch = DBOperation("fetch",self.query_dict,self)
        self._query_dict=None
        self._list=None

    @property
    def addb(self):
        if not self._addb:
            self._addb=self._app_project.addb
        return self._addb
    @property
    def query_dict(self):
        if not self._query_dict:
            config_file=ConfigFile(self.filepath)
            self._query_dict= config_file.properties
        return self._query_dict
    def has_query(self,key):
        return key in self.query_dict

    @property
    def filepath(self):
        if not self._filepath:
            self._filepath = self._app_project.paths["ad_queries"].path
        return self._filepath


    @staticmethod
    def make_from_app_prj(app_project):
        return QueryRunner(app_project =app_project)

    @staticmethod
    def make_from_file(filepath,db=None):
        return QueryRunner(filepath=filepath,emdb=db)

