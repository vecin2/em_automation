import pyperclip
from sql_gen.ui.cli_ui_util import input_with_validation,InputRequester
from sql_gen.emproject import current_emproject
from sql_gen.emproject.emsvn import EMSvn
import os

class Clipboard():
    def on_write(self, sqltask):
        file_path=sqltask.fs_location()
        print("\nFile path '"+file_path+"' copied to clipboard")
        pyperclip.copy(file_path)

class SQLTask(object):
    task_path=""
    def __init__(self, root=current_emproject.root,svnclient=EMSvn(),listener=Clipboard(),input_requester=InputRequester()):
        self.root=root
        self.input_requester = input_requester
        self.svnclient =svnclient
        self.listener = listener

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
        self.__write_file(self.table_data, "tableData.sql")
        self.__write_file(self.__update_sequence_content(), "update.sequence")
        print("\nsql_task wrote under: "+ self.fs_location())
        self.listener.on_write(self)

    def __write_file(self, content, file_full_name):
        final_path = os.path.join(self.fs_location(),file_full_name)
        if not os.path.exists(self.fs_location()):
                os.makedirs(self.fs_location())
        f = open(final_path, "w+")
        f.write(content)
        f.close()
    def __update_sequence_content(self):
        print("Computing update sequence no...")
        update_sequence_no =self.svnclient.revision_number()+1
        print("Update sequence number set to: " +str(update_sequence_no))

        return "PROJECT $Revision: "+str(update_sequence_no)+" $"

    def fs_location(self):
        return os.path.join(self.root, self.task_path)
