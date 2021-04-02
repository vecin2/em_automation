import pathlib
import os


import lxml.etree as ET


def Path(path):
    return pathlib.Path(path)


class UndefinedClassException(Exception):

    """Thrown when the file is not found for a given path"""


class InvalidClassException(Exception):

    """Thrown when the file is found but the format is not parseable"""


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


def parse_doctype(xml):
    lines = xml.split("\n")
    if len(lines) < 2:
        return ""
    doctypeline = lines[1]
    return doctypeline.split(" ")[1]


def is_process(src):
    return "ProcessDefinition" == parse_doctype(src.read_text())


class Repository(object):

    """This class instantiates repository objects from the classpath"""

    def __init__(self, product_path, project_path):
        self.product_path = product_path
        self.project_path = project_path

    def load(self, classpath):
        filepath = self._filepath(classpath)
        try:
            tree = ET.parse(str(Path(filepath)))
            doctype = parse_doctype(tree)
            if doctype == "ProcessDefinition":
                result = ProcessDefinition(tree)
            return result

            return tree
        except ET.XMLSyntaxError:
            raise InvalidClassException(classpath)
        except OSError:
            raise UndefinedClassException(classpath)

    def save(self, cedobject):
        filepath = self._filepath(cedobject.classpath)
        self._create_file(filepath, cedobject.content)

    def _create_file(self, path, contents=None):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w+") as f:
            f.write(contents)
        return path

    def _filepath(self, classpath):
        """it returns the full file path from the object classpath and
        the repository filapath location"""
        relative_filepath = Path(classpath.replace(".", "/") + ".xml")
        return self.project_path / relative_filepath


class CedObject(object):

    """Docstring for CedObject"""

    def __init__(self, classpath, content):
        """TODO: to be defined. """
        self.classpath = classpath
        self.content = content


class InvalidCedObject(CedObject):

    """This object is retrieved when searching or loading for an invalid cedobject"""

    def __init__(self, classpath):
        super().__init__(classpath, "Invalid Object")
