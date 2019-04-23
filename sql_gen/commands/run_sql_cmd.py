import os

from sql_gen.commands import PrintSQLToConsoleCommand

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

class RunSQLCommand(PrintSQLToConsoleCommand):
    def __init__(self, env_vars=os.environ,initial_context=None):
        super().__init__(env_vars= env_vars,
                         initial_context = initial_context)
    def run(self):
        super().run()
        """"""
