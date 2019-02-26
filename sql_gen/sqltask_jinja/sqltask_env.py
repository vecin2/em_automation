from . import globals as template_globals
from . import filters as template_filters
from sql_gen.docugen.env_builder import EnvBuilder
import os

class EMTemplatesEnv():
    def extract_templates_path(self,env_vars):
        templates_path=""
        if 'SQL_TEMPLATES_PATH' in env_vars:
            templates_path =env_vars['SQL_TEMPLATES_PATH']
        else:
            templates_path = os.path.join(env_vars['EM_CORE_HOME'],"sqltask","templates")
        return templates_path

    def make_env(self,templates_path):
        env_builder = EnvBuilder()
        env_builder.set_globals_module(template_globals)\
                   .set_filters_package(template_filters)\
                   .set_fs_path(templates_path)
        return env_builder.build()
