from sql_gen.test.utils.app_runner import PrintSQLToConsoleAppRunner


class RunSQLAppRunner(PrintSQLToConsoleAppRunner):

    def confirmRun(self):
        self.user_inputs("y")
        return self

    def run_sql(self):
        self._run([".", "run-sql"])
        return self
