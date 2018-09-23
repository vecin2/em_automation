import pytest
import os
from sql_gen.sql_module.em_project import SQLTask, EMProject
from sql_gen.ui.cli_ui_util import InputRequester

#set em core home as it used as based to write sql modules
os.environ['EM_CORE_HOME'] = '/em/home' 

def test_fs_example(fs):
    fs.create_file('/var/data/xx1.txt')
    assert os.path.exists('/var/data/xx1.txt')
def test_split():
    assert "home" == "/home".strip("/")

def test_write_creates_table_data_and_update_sequence_file(fs):
    sql_task_path ="/modules/CoreEntity/rewire_search"
    sql_task = SQLTask.make().with_path(sql_task_path).with_table_data("some data");

    sql_task.write()
    
    table_data_path = os.path.join("/em/home/modules/CoreEntity/rewire_search", "tableData.sql")
    assert_file_exist(table_data_path, "some data")

    update_sequence_path = os.path.join("/em/home/modules/CoreEntity/rewire_search", "update.sequence")
    assert_file_exist(update_sequence_path, "PROJECT $Revision: 0 $")

def test_when_joinning_two_paths_starting_in_root_second_path_overrides_first(fs):
    assert "/opt" == os.path.join("/modules","/opt")

def test_when_relative_path_is_given_it_appends_it_to_em_home_path(fs):
    sql_task = SQLTask.make().with_path("modules")
    assert "/em/home/modules" == sql_task.fs_location()

def test_when_linux_root_path_is_given_it_appends_to_em_home_path(fs):
    os.chdir("tmp")
    assert "/tmp" == os.getcwd()
    sql_task = SQLTask.make().with_path("/modules")
    assert "/em/home/modules" == sql_task.fs_location()

def test_set_path_asks_to_override_if_path_already_exists(fs):
    fs.create_file("/em/home/my_module/table_data.sql")
    stub_input_requester = StubInputRequester();
    stub_input_requester.input_entered = "y"

    sql_task = SQLTask(stub_input_requester)
    sql_task.with_path("/my_module")
   
    assert "override" in stub_input_requester.prompted_text

def test_set_path_throws_exception_if_user_does_not_want_to_override(fs):
    with pytest.raises(FileExistsError) as excinfo:
        fs.create_file("/em/home/my_module/table_data.sql")
        stub_input_requester = StubInputRequester();
        stub_input_requester.input_entered = "n"

        sql_task = SQLTask(stub_input_requester)
        sql_task.with_path("/my_module")
    assert "Duplicate sql task" in str(excinfo.value)

def assert_file_exist(file_path, expected_file_content):
    assert os.path.exists(file_path)
    file = open(file_path,"r")
    actual_file_content = file.read()
    assert expected_file_content == actual_file_content

class StubInputRequester(InputRequester):
    def __init__(self):
        self.input_entered = ""
        self.prompted_text =""

    def request_value(self, text,*args):
        self.prompted_text =text
        return self.input_entered



