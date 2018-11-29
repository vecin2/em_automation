from sql_gen.exceptions import ConfigFileNotFoundException
from sql_gen import logger as log_util

class ConfigFile(object):
    def __init__(self, filepath,logger=log_util):
        self.filepath=filepath
        self.logger =logger
        self.properties=self._read_properties(filepath)
    def _read_properties(self,full_path):
        myprops = {}
        try:
            with open(full_path, 'r') as f:
                for line in f:
                    line = line.rstrip() #removes trailing whitespace and '\n'

                    if "=" not in line: continue #skips blanks and comments w/o =
                    if line.startswith("#"): continue #skips comments which contain =
                    k, v = line.split("=", 1)
                    myprops[k] = v
        except FileNotFoundError as e_info:
            self.logger.error("File not found "+str(e_info))
            raise ConfigFileNotFoundException("Config file '"+full_path+"' does not exist")
        return myprops

    def __contains__(self, item):
        return item in self.properties

    def __getitem__(self,name):
        return self.properties[name]


