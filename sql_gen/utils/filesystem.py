import os
from sql_gen.exceptions import InvalidFileSystemPathException

class RelativePath(dict):
    def __init__(self,root,dict):
        self.root= root
        self.paths=dict
    def __getitem__(self,key):
        return os.path.join(self.root,self.paths[key])
    def check(self):
        for key in self.paths:
            self.check_path(self[key])
    def check_path(self,path):
        if not os.path.exists(path):
            raise InvalidFileSystemPathException("Path '"+path+"' does not exist.")

