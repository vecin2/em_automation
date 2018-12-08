import os
from sql_gen.exceptions import InvalidFileSystemPathException

class Path(object):
    def __init__(self,path="",path_type="mandatory"):
        self.path=path
        self.path_type=path_type
    def is_mandatory(self):
        return self.path_type == "mandatory"

class RelativePath(dict):
    def __init__(self,root,dict):
        self.root= root
        self.paths=dict
    def __getitem__(self,key):
        return os.path.join(self.root,self.paths[key].path)
    def check(self):
        for key in self.paths:
            self.check_path(key)
    def check_path(self,key):
        path =self.paths[key]
        if path.is_mandatory() and not os.path.exists(self[key]):
            raise InvalidFileSystemPathException("Path '"+self[key]+"' does not exist.")

