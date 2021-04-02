import os

from sql_gen.app_project import AppProject
from sql_gen.commands import PrintSQLToConsoleCommand
from sql_gen.ui.utils import select_string_noprompt


class RunSQLDisplayer(object):
    def confirm_run_sql(self, sql):
        text = "Are you sure you want to run the above SQL (y/n): "
        return select_string_noprompt(text, ["y", "n"])

    def display_sqltable(self, sqltable):
        print(str(sqltable))


class RunSQLCommand(PrintSQLToConsoleCommand):
    def __init__(
        self,
        env_vars=os.environ,
        context_builder=None,
        displayer=RunSQLDisplayer(),
        template_name=None,
    ):
        # We dont want to run the SQL on print as this command runs it as well
        super().__init__(env_vars=env_vars, context_builder=context_builder)
        self.displayer = displayer
        self.env_vars = env_vars
        self.template_name = template_name
        self.is_select_stmt = False

    def run(self):
        super().run()
        # check if the first stmt in the file is select
        if not self.is_select_stmt and self.user_confirms_run():
            self.run_sql()

    def user_confirms_run(self):
        return self.displayer.confirm_run_sql(self.sql_printed()) == "y"

    def run_sql(self):
        self._db().execute(self.sql_printed(), commit=True, verbose="v")

    def write(self, content, template=None):
        result = super().write(content, template)
        if result:
            self.is_select_stmt = True
            self.displayer.display_sqltable(result)
