import pytest
import os
from sql_module.em_project import SQLTask, EMProject

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

    

def assert_file_exist(file_path, expected_file_content):
    assert os.path.exists(file_path)
    file = open(file_path,"r")
    actual_file_content = file.read()
    assert expected_file_content == actual_file_content

