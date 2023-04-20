from sql_gen.test.utils.app_runner import ApplicationRunner


class PrintSQLToConsoleAppRunner(ApplicationRunner):
    # def __init__(self, fs=None):
    #     super().__init__(fs=fs)

    def print_sql(self, app=None):
        self._run([".", "print-sql"], self.build_app())
        return self

    def assert_printed_sql(self, expected_sql):
        assert expected_sql == self.app.last_command_run.sql_printed()
        return self
