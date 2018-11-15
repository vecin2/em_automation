import os
class RelativePath(dict):
    def __init__(self,root,dict):
        self.root= root
        self.paths=dict
    def __getitem__(self,key):
        return os.path.join(self.root,self.paths[key])

