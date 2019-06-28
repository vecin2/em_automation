import os,sys

from jinja2 import Environment
from jinja2 import FileSystemLoader as JinjaFileSystemLoader
from . import source_inspector

from sql_gen.sqltask_jinja.filters.codepath import codepath
from sql_gen.sqltask_jinja.filters.description import description
from sql_gen.sqltask_jinja.filters.print import print as print_filter
from sql_gen.sqltask_jinja.filters.suggest import suggest
from sql_gen.sqltask_jinja.filters.other import split_uppercase,objectname,objectdir
from jinja2 import StrictUndefined,Undefined,UndefinedError
from jinja2.runtime import missing

class TraceUndefined(StrictUndefined):
    executed_vars={}
    def __init__(self, hint=None, obj=missing, name=None, exc=UndefinedError):
        TraceUndefined.executed_vars[name]=True
        super().__init__(hint = hint,
                         obj= missing,
                         name= name,
                         exc =exc)
    @staticmethod
    def clear_vars():
        TraceUndefined.executed_vars={}

class FileSystemLoader(JinjaFileSystemLoader):
    def __init__(self, searchpath, encoding='utf-8', followlinks=False):
        super().__init__(searchpath,encoding,followlinks)

    def list_templates(self):
        found = set()
        for searchpath in self.searchpath:
            walk_dir = os.walk(searchpath, followlinks=self.followlinks)
            for dirpath, dirnames, filenames in walk_dir:
                for filename in filenames:
                    template = os.path.join(dirpath, filename) \
                        [len(searchpath):].strip(os.path.sep) \
                                          .replace(os.path.sep, '/')
                    if template[:2] == './':
                        template = template[2:]
                    extension=os.path.splitext(template)[1]
                    if template not in found\
                            and (".sql" == extension
                            or ".txt" == extension):
                        found.add(template)
        return sorted(found)

class EnvBuilder(object):
    def __init__(self):
        self.globals_module=None
        self.filters_package=None
        self.path =None
        self.loader = None
        self.env_vars = os.environ

    def set_globals_module(self,module):
        self.globals_module = module
        return self

    def set_filters_package(self,package):
        self.filters_package = package
        return self

    def set_fs_path(self,path):
        self.path = path
        return self

    def set_loader(self, loader):
        self.loader =loader
        return self

    def _get_loader(self):
        if self.loader:
           return self.loader
        else:
           return FileSystemLoader(self.path)

    def build(self):
        env = Environment(
                      loader=self._get_loader(),
                      trim_blocks=True,
                      lstrip_blocks=True,
                      keep_trailing_newline=False, #default
                      undefined=TraceUndefined
                      )
        self._build_globals(env)
        self._build_filters(env)
        return env 
    def _build_globals(self,env):
        if self.globals_module:
            functions =source_inspector.extract_module_functions(self.globals_module)
            env.globals.update(functions)

    def _build_filters(self,env):
        env.filters['codepath']= codepath
        env.filters['description']= description
        env.filters['print']= print_filter
        env.filters['suggest']= suggest
        env.filters['split_uppercase']= split_uppercase
        env.filters['objectname']= objectname
        env.filters['objectdir']= objectdir
        #if self.filters_package:
        #    functions = source_inspector.extract_pkg_funcs_list_by_name(
        #                    self.filters_package,
        #                    "get_template_filter")
        #    env.filters.update(functions)

