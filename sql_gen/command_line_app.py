import argparse
from sql_gen.create_sqltask_app import CreateSQLTaskApp
class CommanLineApp(object):
    """"""
    def __init__(self,create_task_app=None):
        self.create_task_app = create_task_app
    def run (self):
        args = self.parse_args()
        self.create_task_app.set_path(args.dir)
        self.create_task_app.run()
    def parse_args(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-d", "--dir", help="Its the directory where the sql task will be written to. Its a relative path from  $CORE_HOME to, e.g. modules/GSCCoreEntites...")
        return ap.parse_args()

