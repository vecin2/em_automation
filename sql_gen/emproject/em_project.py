import os
import sql_gen
from sql_gen.config import ConfigFile
from .ccadmin import CCAdmin
from sql_gen.exceptions import CCAdminException,ConfigFileNotFoundException,ConfigException,EnvVarNotFoundException,InvalidEnvVarException,InvalidFileSystemPathException
from sql_gen.utils.filesystem import ProjectLayout,Path

class EMConfigID(object):
    def __init__(self,
                 env_name,
                 machine_name,
                 container_name):
        self.env_name = env_name
        self.machine_name = machine_name
        self.container_name = container_name

PATHS={"ccadmin"         : "bin",
       "repo_modules"    : "repository/default",
       "config"          : "work/config",
       "show_config_txt" : "work/config/show-config-txt"
       }
MANDATORY_KEYS=["ccadmin",
                "repo_modules"
               ]


def get_prj_home(env_vars):
    env_name='EM_CORE_HOME'
    help_text="It should contain the path of your current EM project."
    try:
        result = env_vars[env_name]
    except Exception:
        raise EnvVarNotFoundException(env_name,help_text)
    if not result:
        raise EnvVarNotFoundException(env_name,help_text)
    if not os.path.exists(result):
        error_msg ="Environment variable '"+env_name+"' exists "+\
                   "but it points to an invalid path"
        raise ValueError(error_msg)
    return result

def emproject_home(env_vars=os.environ):
    try:
        return get_prj_home(env_vars)
    except Exception as excinfo:
        sql_gen.logger.error(str(excinfo))
        raise excinfo


class EMProject(object):
    def __init__(self,ccadmin_client=None,env_vars=None):
        self.env_vars =env_vars
        self._root = None
        self._paths= None
        self._ccadmin_client = ccadmin_client
        self.emautomation_props={}
        self.default_config_id =None

    @property
    def root(self):
        if not self._paths:
            self._root= emproject_home(self.env_vars)
        return self._root

    @property
    def paths(self):
        if not self._paths:
            self._paths= ProjectLayout(self.root,PATHS)
        return self._paths

    @property
    def ccadmin_client(self):
        if not self._ccadmin_client:
            self._ccadmin_client = CCAdmin(self.paths['ccadmin'].path)
        return self._ccadmin_client

    def set_default_config_id(self,config_id):
        self.default_config_id =config_id

    def config(self,config_id=None):
        if not self.config_path(config_id).exists():
            self._create_config()
        return ConfigFile(self.config_path(config_id).path).properties

    def config_path(self,config_id=None):
        file_name =self._build_config_file_name(config_id)
        result = self.paths['show_config_txt'].join(file_name)
        return result

    def _build_config_file_name(self,config_id):
        actual_config_id=self._actual_config_id(config_id)
        env_name= actual_config_id.env_name
        machine_name= actual_config_id.machine_name
        container_name= actual_config_id.container_name
        return env_name+"-"+machine_name+"-"+container_name+".txt"

    def _actual_config_id(self,config_id):
        if not config_id and not self.default_config_id:
            error_msg ="Try to retrieve configuration but not config_id was specified. You can specify the config by either passing a config_id or by setting a default config_id (environment.name, machine.name and container.name)"
            raise ConfigException(error_msg)
        elif config_id:
            return config_id
        else:
            return self.default_config_id

    def _create_config(self):
        try:
            self.ccadmin_client.show_config("-Dformat=txt")
        except CCAdminException as info:
            error_msg ="Something went wrong while running ccadmin command:\n  "+str(info)
            raise ConfigException(error_msg)

    def prefix(self):
        custom_repo_modules = self._get_repo_custom_modules()
        if not custom_repo_modules:
            raise ValueError("To compute project prefix custom modules must exist under ${em_core_home}/repository/default/, starting with at least three capital letters")
        return self._extract_module_prefix(custom_repo_modules[0])

    def _extract_module_prefix(self, repo_module):
        result = ''
        #module like SPENCoreEntities
        for c in repo_module:
            if c.isupper():
                result +=c
            else:
                break
        #result is now SPENC
        return result[:-1]

    def _get_repo_custom_modules(self):
        repo_modules= self.paths['repo_modules'].listdir()
        result=[]
        for module in repo_modules:
            if len(self._extract_module_prefix(module)) >2:
                result.append(module)
        return result

    def product_layout(self):
        return ProjectLayout(self.config()['product.home'],PATHS)
