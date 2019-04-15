from . import globals as template_globals
from . import filters as template_filters
from sql_gen.app_project import AppProject
from sql_gen.exceptions import EnvVarNotFoundException
from sql_gen.docugen.env_builder import EnvBuilder
import os

class EMTemplatesEnv():
    def get_templates_path(self,env_vars):
        templates_path=""
        templates_path_env_name='SQL_TEMPLATES_PATH'
        em_prj_env_name='EM_CORE_HOME'
        if templates_path_env_name in env_vars:
            templates_path = env_vars[templates_path_env_name]
        else:
             try:
                 app_prj=AppProject(env_vars)
                 templates_path = app_prj.paths["templates"].path
             except:
                 error_msg="Templates path can not be determined from current directory or from environment variables. "+\
                 "Please make sure you running this command from within an EM project folder. Otherwise, if you want to run it from anywhere within your filesystem, add '"+em_prj_env_name+"' to your environment variables (so templates path can be computes) or, add '"+templates_path_env_name+"'."
                 raise ValueError(error_msg)
        return templates_path

    def extract_templates_path(self,env_vars):
        templates_path = self.get_templates_path(env_vars)
        if not os.path.exists(templates_path):
            error_msg="Templates path '"+templates_path+"' does not exist. "+\
            "Make sure the directory is created and it contains templates"
            raise ValueError(error_msg)
        return templates_path

    def make_env(self,templates_path):
        env_builder = EnvBuilder()
        env_builder.set_globals_module(template_globals)\
                   .set_filters_package(template_filters)\
                   .set_fs_path(templates_path)
        return env_builder.build()
