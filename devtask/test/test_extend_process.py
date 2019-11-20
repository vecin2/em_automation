import os
import sys
import pytest
import pathlib

import lxml.etree as ET
from lxml import objectify

from devtask.extend_process import extend_process,main


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

    def file_exists(self,filepath,contents):
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

header ="""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ProcessDefinition [] >
"""
def empty_process():
    root = ET.Element('PackageEntry')

    attribs ={
            "appearsInHistory":"true",
            "cyclic":"false",
            "designNotes":"Undefined",
            "exceptionStrategy":"1",
            "icon":"",
            "isPrivate":"false",
            "logicalDatabaseConnection":"",
            "name":"EmptyProcess",
            "nested":"false",
            "pointOfNoReturn":"false",
            "transactionBehaviour":"TX_NOT_SUPPORTED",
            "version":"10",
            "waitOnChildren":"false"}
    pd =ET.SubElement(root,"ProcessDefinition",attribs)
    attribs ={
            "displayName":"",
             "name":"",
             "x":"16",
             "y":"32",
             }
    #return  header + ET.tostring(root, pretty_print="true",encoding="unicode")
    return ET.tostring(root,
                pretty_print=True,
                xml_declaration=True,
                doctype='<!DOCTYPE ProcessDefinition [] >').decode("utf-8")

def test_empty_process():
    empty_process_template = Path("devtask/test/templates/EmptyProcess.xml")
    parser = ET.XMLParser(remove_blank_text=True)
    et =ET.parse(str(empty_process_template),parser)
    root = et.getroot()
    ET.ElementTree(root).write("output_original.xml",
                             pretty_print=True,
                             xml_declaration=True,
                             encoding="UTF-8",
                             doctype='<!DOCTYPE ProcessDefinition [] >',
                            )
    expected =  ET.tostring(root, pretty_print="true",encoding="unicode",doctype=et.docinfo.doctype)
    empty_process_text = empty_process()

    with open("output.xml","+w") as f:
        f.write(empty_process_text)

    assert  expected == empty_process()

def test_extend_process_by_copy_copies_process_to_project_path(app_runner,fs):
    """"""
    process_path =Path("/repository/default/CoreEntities/EmptyProcess.xml")
    source_content=empty_process()
    fs.create_file(str(process_path), contents=source_content)
    assert process_path.exists()

    target =Path("/repository/default/PRJEntities/Account")
    app_runner.extend_process(process_path,target)
    app_runner.file_exists(target/"EmptyProcess.xml",
                           contents=source_content)
