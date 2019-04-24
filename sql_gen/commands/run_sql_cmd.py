import os

from sql_gen.app_project import AppProject
from sql_gen.commands import PrintSQLToConsoleCommand
from sql_gen.ui.utils import select_string_noprompt

def __init__(self, env_vars=os.environ,
        initial_context=None,
        emprj_path =None,
        templates_path=None):
    if initial_context is None:
        if emprj_path:
            initial_context = init(emprj_path=emprj_path)
        else:
            initial_context=init(AppProject(env_vars=env_vars))
    if templates_path:
        self.templates_path = templates_path
    else:
        self.templates_path=EMTemplatesEnv().extract_templates_path(env_vars)
    self.initial_context =initial_context

class RunSQLDisplayer(object):
    def confirm_run_sql(self,sql):
        text= "Are you sure you want to run the above SQL (y/n): "
        return select_string_noprompt(text,['y','n'])

class RunSQLCommand(PrintSQLToConsoleCommand):
    def __init__(self, env_vars=os.environ,initial_context=None):
        super().__init__(env_vars= env_vars,
                         initial_context = initial_context)
        self.displayer = RunSQLDisplayer()
        self.env_vars = env_vars
    def run(self):
        super().run()
        if self.user_confirms_run():
            self.run_sql()

    def user_confirms_run(self):
        return self.displayer.confirm_run_sql(self.sql_printed()) == 'y'

    def run_sql(self):
        self._db().execute(self.sql_printed(),commit=True)

    def _db(self):
        return self.initial_context["_database"]

