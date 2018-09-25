import os
from sql_gen.ui.cli_ui_util import input_with_validation,InputRequester

class EMProject(object):
    @staticmethod
    def core_home():
        return os.environ['EM_CORE_HOME']



class SQLTask(object):
    def __init__(self, input_requester=InputRequester()):
        self.update_sequence="PROJECT $Revision: 0 $"
        self.input_requester = input_requester

    @staticmethod
    def make(input_requester=InputRequester()):
        sql_task = SQLTask(input_requester)
        return sql_task
    
    def with_path(self, task_path):
        self.task_path = task_path.strip(os.path.sep)
        if os.path.exists(self.fs_location()) and not self._ask_override_file():
            raise FileExistsError("Duplicate sql task")
        return self

    def _ask_override_file(self):
        text= "Are you sure you want to override the path"+ self.fs_location() + " (y/n): " 
        return self.input_requester.request_value(text,"y","n") == "y"

    def with_table_data(self, table_data):
        self.table_data = table_data
        return self

    def write(self):
        print("writing to disk sql_task under: "+ self.fs_location())
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

