import lxml.etree as ET
from devtask.object_factory import new_process_def
import pathlib


def Path(path):
    return pathlib.Path(path)


def xml_str(filepath):
    empty_process_template = Path(filepath)
    parser = ET.XMLParser(remove_blank_text=True)
    et = ET.parse(str(empty_process_template), parser)
    return tostring(et.getroot())


def tostring(element):
    xml_declaration = "<?xml version='1.0' encoding='UTF-8'?>"
    doctype = "<!DOCTYPE ProcessDefinition [] >"
    return (
        xml_declaration
        + "\n"
        + ET.tostring(element, pretty_print="true", encoding="unicode", doctype=doctype)
    )


def test_empty_process():
    assert new_process_def() == xml_str("devtask/test/templates/EmptyProcess.xml")
