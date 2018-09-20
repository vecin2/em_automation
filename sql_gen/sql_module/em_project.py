import os

class EMProject(object):
    @staticmethod
    def core_home():
        return os.environ['EM_CORE_HOME']


class SQLTask(object):
    def __init__(self):
        self.update_sequence="PROJECT $Revision: 0 $"

    @staticmethod
    def make():
        sql_task = SQLTask()
        return sql_task
    
    def with_path(self, task_path):
        self.task_path = task_path.strip(os.path.sep)
        return self

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
