import pytest
import os
from sql_module.em_project import SQLTask, EMProject


def test_creates_update_sequence(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1

def test_image_file(fs):
    fs.create_file('/var/data/xx1.txt')
    assert os.path.exists('/var/data/xx1.txt')

def test_create_sql_task(fs):
    sql_task_path ="/modules/CoreEntiy/rewire_search"
    sql_task = SQLTask.make().path(sql_task_path).with_table_data("some data");
    sql_task.write()
    
    full_task_path = os.path.join(EMProject.core_home(), sql_task_path)
    table_data_path = os.path.join(full_task_path, "tableData.sql")
    assert_file_exist(table_data_path, "some data")
    update_sequence_path = os.path.join(full_task_path, "update.sequence")
    assert_file_exist(update_sequence_path, "PROJECT $Revision: 0 $")

def assert_file_exist(file_path, expected_file_content):
    assert os.path.exists(file_path)
    file = open(file_path,"r")
    actual_file_content = file.read()
    assert expected_file_content == actual_file_content

