import os
import sys
import pytest
import pathlib

import lxml.etree as ET
from lxml import objectify

from devtask.extend_process import extend_process,main
from devtask.object_factory import new_process_def

@pytest.mark.skip
def test_parse_doctype():
    filepath =Path(__file__).parent
    process_path =filepath/Path("templates/EmptyProcess.xml")
    et = ET.parse(str(process_path))
    assert "bla" ==et.docinfo.doctype



def Path(path):
    return pathlib.Path(path)

class AppRunner(object):
    def __init__(self,capsys):
        self.capsys = capsys

    def extend_process(self,process_path,target=None):
        sys.argv=[]
        sys.argv.append("")
        sys.argv.append(str(process_path))
        sys.argv.append(str(target))
        return main()

    def displays_message(self,message):
        assert self.capsys.readouterr().out == message

    def assert_file_exists(self,filepath,contents):
        if not filepath.exists():
            assert False, "'"+str(filepath)+"' does not exists"
        assert contents == str(filepath.read_text())

@pytest.fixture
def app_runner(fs,capsys):
    app_runner = AppRunner(capsys)
    yield app_runner

def test_returnserror_when_invalid_path(app_runner):
    process_path =Path("/repository/default/Account/NonExitingProcess.xml")
    app_runner.extend_process(process_path)
    app_runner.displays_message("No process found under '"+str(process_path)+"'\n")

def test_returnserror_when_file_not_a_process(app_runner,fs):
    process_path =Path("/repository/default/Account/NonExitingProcess.xml")

    fs.create_file(str(process_path), contents="Invalid xml")
    app_runner.extend_process(process_path)
    app_runner.displays_message("Not a valid xml process found under '"+str(process_path)+"'\n")


def test_extend_process_by_copy_copies_process_to_project_path(app_runner,fs):
    """"""
    process_path =Path("/repository/default/CoreEntities/EmptyProcess.xml")
    source_content=new_process_def()
    fs.create_file(str(process_path), contents=source_content)
    target =Path("/repository/default/PRJEntities/Account")
    app_runner.extend_process(process_path,target)
    app_runner.assert_file_exists(target/"EmptyProcess.xml",
                           contents=source_content)

