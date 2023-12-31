from sqltask.shell.shell_factory import InteractiveSQLTemplateRunnerBuilder


class RunSQLCommand:
    def __init__(self, project=None):
        self.project = project

    def run(self):
        builder = InteractiveSQLTemplateRunnerBuilder.default(self.project)
        builder.commit_rendered_sql()
        shell = builder.build()
        shell.run()
