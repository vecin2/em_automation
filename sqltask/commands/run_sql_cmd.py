import os

from sqltask.commands import PrintSQLToConsoleCommand


class RunSQLCommand(PrintSQLToConsoleCommand):
    def __init__(
        self,
        env_vars=os.environ,
        templates_path=None,
        context_builder=None,
    ):
        # We dont want to run the SQL on print as this command runs it as well
        super().__init__(
            templates_path=templates_path,
            context_builder=context_builder,
        )
        self.env_vars = env_vars
        self.commit_changes = True

    def run(self):
        super().run()

    def run_sql(self):
        self._db().execute(self.sql_printed(), commit=True, verbose="v")

    def write(self, content, template=None):
        result = super().write(content, template)
        if result:
            self.is_select_stmt = True
        return result
