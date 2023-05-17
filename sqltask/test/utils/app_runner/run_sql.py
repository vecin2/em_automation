from sqltask.test.utils.app_runner import PrintSQLToConsoleAppRunner


class RunSQLAppRunner(PrintSQLToConsoleAppRunner):

    def confirm_run(self):
        self.user_inputs("y")
        return self

    def run_sql(self):
        self._run([".", "run-sql"])
        return self
