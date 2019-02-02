from jinja2 import Environment, FileSystemLoader
import os,sys
from . import source_inspector


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

    def set_env_vars(self,env_vars):
        self.env_vars
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
                      keep_trailing_newline=False #default
                      )
        self._build_globals(env)
        self._build_filters(env)
        return env 
    def _build_globals(self,env):
        if self.globals_module:
            functions =source_inspector.extract_module_functions(self.globals_module)
            env.globals.update(functions)

    def _build_filters(self,env):
        if self.filters_package:
            functions = source_inspector.extract_pkg_funcs_list_by_name(
                            self.filters_package,
                            "get_template_filter")
            env.filters.update(functions)

