import os
import sys
import pytest
import pathlib
import io

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

def new_process_def(parent):
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
    return ET.SubElement(parent,"ProcessDefinition",attribs)

def empty_process():
    root = ET.Element('PackageEntry')
    process_def = new_process_def(root)
    ET.SubElement(process_def,"StartNode",displayName="",name="",x="16",y="32")
    ET.SubElement(process_def,"EndNode",displayName="",name="",x="240",y="32")
    transition = ET.SubElement(process_def,"Transition",isExceptionTransition="false")
    ET.SubElement(transition,"StartNodeReference",name="")
    ET.SubElement(transition,"EndNodeReference",name="")
    graph_node_list = ET.SubElement(transition,"GraphNodeList",name="")
    graph_node = ET.SubElement(graph_node_list,
                               "GraphNode",
                               icon="",
                               isLabelHolder="true",
                               label="",
                               name="",
                               x="128",
                               y="32")
    ET.SubElement(process_def,"BuilderInfo",name="")
    ET.SubElement(process_def,"TopicScope",defineTopicScope="false",name="")
    return ET.tostring(root,
                pretty_print=True,
                doctype='<!DOCTYPE ProcessDefinition [] >',
                encoding ="UTF-8",
                xml_declaration=True,
                ).decode("utf-8")

def xml_str(filepath):
    empty_process_template = Path(filepath)
    parser = ET.XMLParser(remove_blank_text=True)
    et =ET.parse(str(empty_process_template),parser)
    return tostring(et.getroot())

def tostring(element):
    xml_declaration ="<?xml version='1.0' encoding='UTF-8'?>"
    doctype='<!DOCTYPE ProcessDefinition [] >'
    return xml_declaration+ "\n" +ET.tostring(element, pretty_print="true",encoding="unicode",doctype=doctype)

def test_empty_process():
    assert  empty_process() == xml_str("devtask/test/templates/EmptyProcess.xml")

def test_parse_doctype():
    filepath =Path(__file__).parent
    process_path =filepath/Path("templates/EmptyProcess.xml")
    et = ET.parse(str(process_path))
    assert "bla" ==et.docinfo.doctype

def test_extend_process_by_copy_copies_process_to_project_path(app_runner,fs):
    """"""
    process_path =Path("/repository/default/CoreEntities/EmptyProcess.xml")
    source_content=empty_process()
    fs.create_file(str(process_path), contents=source_content)
    target =Path("/repository/default/PRJEntities/Account")
    app_runner.extend_process(process_path,target)
    app_runner.assert_file_exists(target/"EmptyProcess.xml",
                           contents=source_content)
