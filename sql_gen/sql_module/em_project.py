import os
from sql_gen.ui.cli_ui_util import input_with_validation,InputRequester

class EMProject(object):
    @staticmethod
    def core_home():
        try:
            return os.environ['EM_CORE_HOME']
        except Exception:
            raise AttributeError("EM_CORE_HOME must added to environment variables and it should contain the path of your current em project")

    @staticmethod
    def prefix():
        em_project = EMProject()
        custom_repo_modules = em_project._get_repo_custom_modules()
        if not custom_repo_modules:
            raise ValueError("To compute project prefix custom modules must exist under ${em_core_home}/repository/default/, starting with at least three capital letters")
            
        return em_project._extract_module_prefix(custom_repo_modules[0])

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
        comm_sep_path =EMProject.core_home()+",repository,default"
        repo_modules_arr= comm_sep_path.split(",") 
        repo_modules_path= os.path.join(*repo_modules_arr)
        if not os.path.exists(repo_modules_path) or not os.listdir(repo_modules_path):
            return []
        #if there is at least one module created
        return [name for name in os.listdir(repo_modules_path)
           if os.path.isdir(os.path.join(repo_modules_path, name))]

class SQLTask(object):
    def __init__(self, input_requester=InputRequester()):
        self.update_sequence="PROJECT $Revision: 0 $"
        self.input_requester = input_requester
        #make sure em_core_home is setup
        EMProject.core_home()

    @staticmethod
    def make(input_requester=InputRequester()):
        sql_task = SQLTask(input_requester)
        return sql_task
    
    def with_path(self, task_path):
        #strip as well "/" as we could run in windows within GitBash or CygWin
        self.task_path = task_path.strip(os.path.sep).strip("/")
        if os.path.exists(self.fs_location()) and not self._ask_override_file():
            raise FileExistsError("Duplicate sql task")
        return self

    def _ask_override_file(self):
        text= "Are you sure you want to override the path '"+ self.fs_location() + "' (y/n): " 
        return self.input_requester.request_value(text,"y","n") == "y"

    def with_table_data(self, table_data):
        self.table_data = table_data
        return self

    def write(self):
        print("\nWriting to disk sql_task under: "+ self.fs_location())
        self.__write_file(self.table_data, "tableData.sql")
        self.__write_file(self.update_sequence, "update.sequence")

    def __write_file(self, content, file_full_name):
        final_path = os.path.join(self.fs_location(),file_full_name)
        if not os.path.exists(self.fs_location()):
                os.makedirs(self.fs_location())
        f = open(final_path, "w+")
        f.write(content)
        f.close()

    def fs_location(self):
        return os.path.join(EMProject.core_home(), self.task_path)

