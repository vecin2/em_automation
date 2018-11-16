import os
from sql_gen.logger import logger
from sql_gen.config import ConfigFile
from sql_gen.exceptions import CCAdminException,ConfigFileNotFoundException,ConfigException,EnvironmentVarNotFoundException,InvalidEnvVarException,InvalidFileSystemPathException
from sql_gen.utils.filesystem import RelativePath

class CCAdmin(object):
    show_config_content=""
    def __init__(self,root):
        self.root =root

    def show_config(self, params):
        logger.debug("Running ccadmin show-config "+params)
        result = self._run_ccadmin("show-config "+params)
        logger.debug("End Running ccadmin show-config")
        return result

    def _run_ccadmin(self, command_and_args):
        result = os.system(self._ccadmin_file() +" "+command_and_args)
        if result ==0:
            return result
        raise CCAdminException("Failed when running '"+self._ccadmin_file()+" "+ command_and_args+"'")
    def _ccadmin_file(self):
        ccadmin_file_name ="ccadmin."+self._ccadmin_file_ext()
        ccadmin_path=os.path.join(self.root, ccadmin_file_name)
        logger.debug("ccadmin found under: "+ ccadmin_path)
        return ccadmin_path

    def _ccadmin_file_ext(self):
        logger.debug("Checking OS name: "+ os.name)
        if os.name == 'nt':
            return "bat"
        else:
            return "sh"

def to_path(filesystem_path):
    repo_modules_arr= filesystem_path.split(",") 
    return os.path.join(*repo_modules_arr)

class EMConfigID(object):
    def __init__(self,
                 env_name,
                 machine_name,
                 container_name):
        self.env_name = env_name
        self.machine_name = machine_name
        self.container_name = container_name

PATHS={"ccadmin"     : "bin",
       "config"      : "work/config/show-config-txt",
       "repo_modules": "repository/default"
       }

def emproject_home():
    try:
        result = os.environ['EM_CORE_HOME']
    except Exception:
        raise EnvironmentVarNotFoundException("EM_CORE_HOME","contains the path of you current EM project.")
    if not result:
        raise EnvironmentVarNotFoundException("EM_CORE_HOME","contains the path of you current EM project.")
    relative_path =RelativePath(result,PATHS)
    try:
        relative_path.check()
    except InvalidFileSystemPathException as excinfo:
        raise InvalidEnvVarException("Are you sure 'EM_CORE_HOME' points to a valid EM installation? "+ str(excinfo))
    return result


class EMProject(object):
    def __init__(self,root=None,ccadmin_client=None):
        if not root:
            root = emproject_home()
        self.root = root
        self.paths= RelativePath(self.root,PATHS)
        if not ccadmin_client:
            ccadmin_client = CCAdmin(self.paths['ccadmin'])
        self.ccadmin_client = ccadmin_client
        self.ccadmin_client =ccadmin_client
        self.emautomation_props={}
        self.default_config_id =None

    def set_default_config_id(self,config_id):
        self.default_config_id =config_id

    def config(self,config_id=None):
        if not os.path.exists(self.config_path(config_id)):
            self._create_config()
        config_content = ConfigFile(self.config_path(config_id)).properties
        return config_content

    def config_path(self,config_id=None):
        file_name =self._build_config_file_name(config_id)
        result = os.path.join(self.paths['config'],file_name)
        logger.info("Returning  em config path: "+ result)
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
    def product_prj(self):
        return EMProject(self.prop_val('product.home'))

    def prop_val(self,prop_name):
        return self.config()[prop_name]

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
        repo_modules= self._get_repo_modules()
        result=[]
        for module in repo_modules:
            if len(self._extract_module_prefix(module)) >2:
                result.append(module)
        return result

    def repo_modules_path(self):
        full_path= self.root +",repository,default"
        return to_path(full_path)

    def _get_repo_modules(self):
        repo_modules_path= self.paths['repo_modules']
        if not os.path.exists(repo_modules_path) or not os.listdir(repo_modules_path):
            return []
        #if there is at least one module created
        return [name for name in os.listdir(repo_modules_path)
           if os.path.isdir(os.path.join(repo_modules_path, name))]


