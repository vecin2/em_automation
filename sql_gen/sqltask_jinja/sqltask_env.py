from sql_gen.docugen.env_builder import EnvBuilder

from . import filters as template_filters
from . import globals as template_globals


class EMTemplatesEnv:
    def __init__(self, templates_path):
        self.templates_path = templates_path
        self._jinja_environment = None

    def _make_env(self):
        env_builder = EnvBuilder()
        env_builder.set_globals_module(template_globals).set_filters_package(
            template_filters
        ).set_fs_path(self.templates_path)
        return env_builder.build()

    def _get_environment(self):
        if not self._jinja_environment:
            self._jinja_environment = self._make_env()
        return self._jinja_environment

    def get_template(self, template_name):
        return self._get_environment().get_template(template_name)

    def list_templates(self, extensions=None, filter_func=None):
        return self._get_environment().list_templates(extensions, filter_func)
