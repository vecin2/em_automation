import os

def emproject_home():
    try:
        return os.environ['EM_CORE_HOME']
    except Exception:
        raise AttributeError("EM_CORE_HOME must added to environment variables and it should contain the path of your current em project")

class EMProject(object):
    CONFIG_PATH_AD_LOCAL='work/config/show-config-txt/localdev-localhost-ad.txt'
    EMAUTOMATION_CONFIG_PATH='config/local.properties'

    def __init__(self,root=emproject_home(),ccadmin_client=None):
        self.root = root
        self.ccadmin_client =ccadmin_client
        self.emautomation_props={}

    def _emautomation_config(self):
        if not self.emautomation_props:
            self.emautomation_props = self._read_properties(self.EMAUTOMATION_CONFIG_PATH)
        return self.emautomation_props

    def config_path(self):
        env_name= self._emautomation_config()['emautomation.environment.name']
        machine_name= self._emautomation_config()['emautomation.machine.name']
        container_name= self._emautomation_config()['emautomation.container.name']
        return "work/config/show-config-txt/"+env_name+"-"+machine_name+"-"+container_name+".txt" 

    def config(self):
        if not self._exists(self.config_path()):
            self.ccadmin_client.show_config()
        config_content = self._read_properties(self.config_path())
        return config_content

    def _exists(self,relative_path):
        full_path = os.path.join(self.root, relative_path)
        return os.path.exists(full_path)

    def _read_properties(self,relative_path):
        full_path = os.path.join(self.root, relative_path)
        myprops = {}
        with open(full_path, 'r') as f:
            for line in f:
                line = line.rstrip() #removes trailing whitespace and '\n' 

                if "=" not in line: continue #skips blanks and comments w/o =
                if line.startswith("#"): continue #skips comments which contain =
                k, v = line.split("=", 1)
                myprops[k] = v
        return myprops

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

    def _get_repo_modules(self):
        comm_sep_path =self.root+",repository,default"
        repo_modules_arr= comm_sep_path.split(",") 
        repo_modules_path= os.path.join(*repo_modules_arr)
        if not os.path.exists(repo_modules_path) or not os.listdir(repo_modules_path):
            return []
        #if there is at least one module created
        return [name for name in os.listdir(repo_modules_path)
           if os.path.isdir(os.path.join(repo_modules_path, name))]


current_emproject = EMProject()
