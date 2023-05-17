from sqltask.test.utils.app_runner import ApplicationRunner


class PrintSQLToConsoleAppRunner(ApplicationRunner):
    def print_sql(self, app=None):
        self._run([".", "print-sql"])
        return self

    def assert_printed_sql(self, expected_sql):
        assert expected_sql == self.app.last_command_run.sql_printed()
        # assert expected_sql == self.console_printer.rendered_sql
        return self
