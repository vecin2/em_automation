from sqltask.docugen.env_builder import EnvBuilder, FileSystemLoader, TemplateLibraryLoader

from . import filters as template_filters
from . import globals as template_globals


class EnvironmentFactory:
    def make_filesystem_env(self, templates_path):
        env_builder = EnvBuilder()
        env_builder.set_globals_module(template_globals).set_filters_package(
            template_filters
        ).set_loader(FileSystemLoader(templates_path))
        return env_builder.build()

    def make_library_env(self, library):
        env_builder = EnvBuilder()
        env_builder.set_globals_module(template_globals).set_filters_package(
            template_filters
        ).set_loader(TemplateLibraryLoader(library))
        return env_builder.build()

class EMTemplatesEnv:
    def __init__(self, library):
        self.library = library
        self._jinja_environment = None

    def _make_env(self):
        return EnvironmentFactory().make_library_env(self.library)

    def _get_environment(self):
        if not self._jinja_environment:
            self._jinja_environment = self._make_env()
        return self._jinja_environment

    def get_template(self, template_name):
        return self._get_environment().get_template(template_name)

    def _list_templates(self, extensions=None, filter_func=None):
        return self._get_environment().list_templates(extensions, filter_func)

    def list_visible_templates(self):
        return self._list_templates(filter_func=self.list_templates_filter)

    def list_templates_filter(self, template_name):
        if "hidden_templates" not in template_name:
            return True

    def loader(self):
        return self._get_environment().loader
