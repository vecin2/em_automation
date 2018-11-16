import pytest
import os
from sql_gen.emproject import SQLTask,emproject_home
from sql_gen.ui.cli_ui_util import InputRequester
from sql_gen import current_emproject

#set em core home as it used as based to write sql modules
class FakeEMSvn(object):
    def __init__(self,force_rev_number):
        self.force_rev_number = force_rev_number

    def revision_number(self):
        return int(self.force_rev_number);

class StubInputRequester(InputRequester):
    def __init__(self,input_entered="y"):
        self.input_entered = input_entered
        self.prompted_text =""

    def request_value(self, text,*args):
        self.prompted_text =text
        return self.input_entered

class FakeSQLTaskListener(object):
    def __init__(self):
        self.invoked_on_write=False

    def on_write(self,sqltask):
        self.invoked_on_write=True

def make_testable_sqltask(root,svnclient=FakeEMSvn("3"),\
                          listener=FakeSQLTaskListener(),\
                          input_requester=InputRequester()):
    return SQLTask(root,svnclient,listener,input_requester)

def test_split():
    assert "home" == "/home".strip("/")

def test_when_joinning_two_paths_starting_in_root_second_path_overrides_first(fs):
    assert "/opt" == os.path.join("/modules","/opt")

def test_sets_root():
    sqltask = SQLTask("/em/home/testsqltask/")
    assert "/em/home/testsqltask/" == sqltask.root

def test_defaults_root_to_current_emproject():
    sqltask = SQLTask()
    assert current_emproject.root == sqltask.root

def test_set_path_appends_to_root(fs):
    sql_task = make_testable_sqltask("/em/home").with_path("modules")
    assert "/em/home/modules" == sql_task.fs_location()

def test_set_path_apprends_to_root_even_if_starts_with_forward_slash(fs):
    sql_task = make_testable_sqltask("/em/home").with_path("/modules")
    assert "/em/home/modules" == sql_task.fs_location()

def test_write_creates_table_data_and_update_sequence_file_and_notifies_listener(fs):
    fake_listener = FakeSQLTaskListener()
    fake_svnclient = FakeEMSvn("3")
    sql_task = make_testable_sqltask("/em/home",\
                                    fake_svnclient,\
                                    fake_listener)
    sql_task.with_table_data("some data").with_path("modules/A")

    sql_task.write()

    assert_file_exist("/em/home/modules/A/tableData.sql",
                      "some data")
    #it should the next number to the current rev number
    assert_file_exist("/em/home/modules/A/update.sequence",\
                      "PROJECT $Revision: 4 $")
    assert fake_listener.invoked_on_write

def test_set_path_asks_to_override_if_path_already_exists(fs):
    fs.create_file("/em/home/my_module/table_data.sql")
    stub_input_requester = StubInputRequester("y");

    sql_task = SQLTask("/em/home",None,None,stub_input_requester)
    sql_task.with_path("/my_module")

    assert "override" in stub_input_requester.prompted_text

def test_set_path_throws_exception_if_user_does_not_want_to_override(fs):
    with pytest.raises(FileExistsError) as excinfo:
        fs.create_file("/em/home/my_module/table_data.sql")
        stub_input_requester = StubInputRequester("n");
        sql_task = SQLTask("/em/home",None,None,stub_input_requester)
        sql_task.with_path("/my_module")

    assert "Duplicate sql task" in str(excinfo.value)

def assert_file_exist(file_path, expected_file_content):
    assert os.path.exists(file_path)
    file = open(file_path,"r")
    actual_file_content = file.read()
    assert expected_file_content == actual_file_content

