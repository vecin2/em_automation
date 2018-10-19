import os

def emproject_home():
    try:
        return os.environ['EM_CORE_HOME']
    except Exception:
        raise AttributeError("EM_CORE_HOME must added to environment variables and it should contain the path of your current em project")

class EMProject(object):
    def __init__(self,root=emproject_home()):
        self.root = root

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
