import os

from jinja2 import Environment
from jinja2 import FileSystemLoader as JinjaFileSystemLoader
from jinja2 import StrictUndefined, UndefinedError
from jinja2.runtime import missing

from sqltask.sqltask_jinja import globals as globals_module
from sqltask.sqltask_jinja.filters.codepath import codepath
from sqltask.sqltask_jinja.filters.description import description
from sqltask.sqltask_jinja.filters.filepath import filepath
from sqltask.sqltask_jinja.filters.other import (objectdir, objectname,
                                                 split_uppercase)
from sqltask.sqltask_jinja.filters.print import print as print_filter
from sqltask.sqltask_jinja.filters.suggest import suggest

from . import source_inspector


class TraceUndefined(StrictUndefined):
    executed_vars = {}

    def __init__(self, hint=None, obj=missing, name=None, exc=UndefinedError):
        TraceUndefined.executed_vars[name] = True
        super().__init__(hint=hint, obj=missing, name=name, exc=exc)

    @staticmethod
    def clear_vars():
        TraceUndefined.executed_vars = {}


class TemplateLibraryLoader(JinjaFileSystemLoader):
    def __init__(self, library, encoding="utf-8", followlinks=False):
        print(f"Templates loaded from '{library.templates_path}'")
        self.library = library
        super().__init__(str(library.templates_path), encoding, followlinks)

    def list_templates(self):
        templates = super().list_templates()
        result = set()
        for template in templates:
            if self.library.is_template_path(template):
                result.add(template)
        return result


class FileSystemLoader(JinjaFileSystemLoader):
    def __init__(self, searchpath, encoding="utf-8", followlinks=False):
        print(f"Templates loaded from '{searchpath}'")
        super().__init__(searchpath, encoding, followlinks)

    def list_templates(self):
        templates = super().list_templates()
        result = set()

        for template in templates:
            extension = os.path.splitext(template)[1]
            if ".sql" == extension or ".txt" == extension or ".groovy" == extension:
                result.add(template)
        return result


class EnvBuilder(object):
    def __init__(self):
        self.globals_module = None
        self.filters_package = None
        self.path = None
        self.loader = None
        self.env_vars = os.environ

    def set_globals_module(self, module):
        self.globals_module = module
        return self

    def _get_globals_module(self):
        # default to globals module if not passed
        if not self.globals_module:
            self.globals_module = globals_module
        return self

    def set_filters_package(self, package):
        self.filters_package = package
        return self

    def set_loader(self, loader):
        self.loader = loader
        return self

    def _get_loader(self):
        return self.loader

    def build(self):
        env = Environment(
            loader=self._get_loader(),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=False,  # default
            undefined=TraceUndefined,
        )
        self._build_globals(env)
        self._build_filters(env)
        return env

    def _build_globals(self, env):
        if self.globals_module:
            functions = source_inspector.extract_module_functions(self.globals_module)
            env.globals.update(functions)

    def _build_filters(self, env):
        env.filters["codepath"] = codepath
        env.filters["filepath"] = filepath
        env.filters["description"] = description
        env.filters["print"] = print_filter
        env.filters["suggest"] = suggest
        env.filters["split_uppercase"] = split_uppercase
        env.filters["objectname"] = objectname
        env.filters["objectdir"] = objectdir
        # if self.filters_package:
        #    functions = source_inspector.extract_pkg_funcs_list_by_name(
        #                    self.filters_package,
        #                    "get_template_filter")
        #    env.filters.update(functions)
