from . import globals as template_globals
from . import filters as template_filters
from sql_gen.exceptions import EnvVarNotFoundException
from sql_gen.docugen.env_builder import EnvBuilder
import os

class EMTemplatesEnv():
    def extract_templates_path(self,env_vars):
        templates_path=""
        templates_path_env_name='SQL_TEMPLATES_PATH'
        em_prj_env_name='EM_CORE_HOME'
        if templates_path_env_name in env_vars:
            templates_path =env_vars[templates_path_env_name]
        elif em_prj_env_name in env_vars:
            templates_path = os.path.join(env_vars[em_prj_env_name],"sqltask","templates")
        else:
            error_msg="Templates path can not be determined from environment variables. "+\
            "Please add '"+em_prj_env_name+"' to your environment variables "+\
            "(so templates path can be computes)"\
            "or, explicetely  add '"+templates_path_env_name+"'."
            raise ValueError(error_msg)
        return templates_path


    def make_env(self,templates_path):
        env_builder = EnvBuilder()
        env_builder.set_globals_module(template_globals)\
                   .set_filters_package(template_filters)\
                   .set_fs_path(templates_path)
        return env_builder.build()
