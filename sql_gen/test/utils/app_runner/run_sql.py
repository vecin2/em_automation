from sql_gen.test.utils.app_runner import PrintSQLToConsoleAppRunner


class RunSQLAppRunner(PrintSQLToConsoleAppRunner):
    """"""

    # def __init__(self, fs):
    #     super().__init__(fs=fs)
    #
    # def assert_prints(self, expected_text):
    #     assert self.displayer.printed_text == expected_text
    #     return self

    def confirmRun(self):
        self.user_inputs("y")
        return self

    def run_sql(self):
        self._run([".", "run-sql"])
        return self
