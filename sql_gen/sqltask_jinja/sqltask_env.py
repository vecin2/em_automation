from . import globals as template_globals
from . import filters as template_filters
from sql_gen.docugen.env_builder import EnvBuilder
import os

class EMTemplatesEnv():
    def get_templates_path(self,env_vars):
        templates_path=""
        if 'SQL_TEMPLATES_PATH' in env_vars:
            templates_path =env_vars['SQL_TEMPLATES_PATH']
        else:
            templates_path = os.path.join(env_vars['EM_CORE_HOME'],"sqltask","templates")
        print("\nLoading templates from '" + templates_path+"':")
        return templates_path

    def get_env(self,env_vars=os.environ):
        env_builder = EnvBuilder()
        env_builder.set_env_vars(env_vars)\
                   .set_globals_module(template_globals)\
                   .set_filters_package(template_filters)\
                   .set_fs_path(self.get_templates_path(env_vars))
        return env_builder.build()
