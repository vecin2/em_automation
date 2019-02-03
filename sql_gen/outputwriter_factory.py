from sql_gen.create_sqltask_command import CreateSQLTaskCommand
import argparse

class ConsoleWritter(object):
    def __init__(self):
        self.content=""
        self.type="console"

    def write(self,content):
        self.content+=content
        print(content)

class FileWriter(object):
    def __init__(self,path):
        self.content=""
        self.path=path
        self.type="file"

    def write(self,content):
        self.content+=content
        print(content)

class OutputWriterFactory(object):
    def __init__(self):
        self.content=""

    def make(self):
        args =self.parse_args()
        path = args.dir
        if path:
            return FileWriter(path)
        else:
            return ConsoleWritter()

    def parse_args(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-d", "--dir", help="Its the directory where the sql task will be written to. Its a relative path from  $CORE_HOME to, e.g. modules/GSCCoreEntites...")
        return ap.parse_args()

