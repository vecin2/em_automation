import re

import os
import sql_gen 

class ConfigFile(object):
    def __init__(self, filepath,logger=None):
        if logger is None:
            self.logger = sql_gen.logger
        else:
            self.logger = logger
        self.filepath=filepath
        self.dict_props=None

    @property
    def properties(self):
        if not self.dict_props:
            self.dict_props= self._read_properties(self.filepath)
        return self.dict_props

    def _read_properties(self,full_path):
        myprops = {}
        if not os.path.exists(full_path):
            raise FileNotFoundError("Try to load config file '"+full_path+"' but it does not exist")
        with open(full_path, 'r') as f:
                for line in f:
                    line = line.rstrip() #removes trailing whitespace and '\n'

                    if "=" not in line: continue #skips blanks and comments w/o =
                    if line.startswith("#"): continue #skips comments which contain =
                    k, v = line.split("=", 1)
                    myprops[k] = v
        return myprops

    def get(self,key,default_value):
        return self.properties.get(key,default_value)

    def __contains__(self, item):
        return item in self.properties

    def __getitem__(self,name):
        return self._resolve(self.properties[name])

    def _resolve(self,value):
        if value.startswith('${') and value.endswith('}'):
                    var_name= value[value.find("${")+2:value.find("}")]
                    if var_name in self:
                        return self[var_name]
                    return ""
        return value
