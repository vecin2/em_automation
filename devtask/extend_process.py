import pathlib

from shutil import copyfile
import os
import sys
import io

import lxml.etree as ET

from sql_gen.app_project import AppProject
from sql_gen.emproject import EMProject

from sql_gen.ui.utils import select_string_noprompt

PurePosixPath = pathlib.PurePosixPath
def parse_doctype(xml):
    lines =xml.split("\n")
    if len(lines)< 2:
        return ""
    doctypeline =lines[1]
    return doctypeline.split(" ")[1]

def is_process(src):
    return "ProcessDefinition" == parse_doctype(src.read_text())

def abspath(repo_path):
    return RepoPath(str(repo_path))
    str_path = str(repo_path)

    return str_path.replace(".","/")
WindowsPath = pathlib.WindowsPath
PosixPath = pathlib.PosixPath
Path = pathlib.Path
class RepoPath(object):
    def __init__(self,path):
        repo_location =Path("/em/project/myproject/repository/default")
        self.abspath = repo_location / path
    def __str__(self):
        return self.abspath.__str__()
    def exists(self):
        return self.abspath.exists()
    def read_text(self):
        return self.abspath.read_text()
    #def __new__(cls,*args):
    #  full_path = str("/em/project/myproject/repository/default"/args[0])
    #  cls = WindowsPath if os.name == 'nt' else PosixPath
    #  self = cls._from_parts([full_path], init=False)
    #  if not self._flavour.is_supported:
    #     raise NotImplementedError("cannot instantiate %r on your system"
    #                    % (cls.__name__,))
    #  self._init()
    #  return self

app_project= None
def get_app_project():
    if not app_project:
        app_project =AppProject()
    return app_project
def extend_process(src,dst=None):
    #src = Path(src)
    
    path=get_app_project().product_layout()['repo_modules'].path+"/"+src
    #path=product_path+"/repository/default/"+src
    src = Path(path)
    if not dst:
        dst ="/some/default/value/to/compute"
    dst = Path(dst)
    if not src.exists():
    #if not os.path.exists(src):
        print("No process found under '"+str(src)+"'")
    elif not is_process(src):
        print("Not a valid xml process found under '"+str(src)+"'")
    else:
        print("Extending process under '"+str(src)+"'")
        prompt_text="Destination process already exists, would you like to override it (y/n)?"
        if not dst:
            dst_input =input("Enter the dst")
            if not dst_input:
                dst_input="/repository/default/PRJEntities/Account2"
            dst=pathlib.Path(dst_input)
        if not dst.exists() or select_string_noprompt(prompt_text,['y','n']) == 'y':
            _copy_process(src,dst)

def _copy_process(src,dst):
    src = str(src)
    dst = str(dst)
    os.makedirs(dst, exist_ok=True)
    dst =dst + "/" +os.path.basename(src)
    copyfile(src, dst)
    print("Extension created under '"+str(dst)+"'")

def main():
    src = pathlib.Path(sys.argv[2])
    if len(sys.argv)>3:
        dst = pathlib.Path(sys.argv[3])
    else:
        dst = None
    extend_process(src,dst)

# Run it only if called from the command line
if __name__ == '__main__':
        main()
