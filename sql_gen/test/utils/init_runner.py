import sys


class InitAppRunner(AppRunner):
    def __init__(self, fs=None):
        super().__init__(fs=fs)

    def run(self, app=None):
        self._run([".", "init"], app=app)
        return self

    def _run(self, args, app=None):
        sys.argv = args
        # sys.stdin = StringIO(self._user_input_to_str())
        if not app:
            app = CommandLineSQLTaskApp(
                self._make_command_factory(),
                project_home_locator=ProjectHomeLocator(),
                logger=FakeLogger(),
            )
        app.run()

    def _make_command_factory(self):
        return CommandFactory(self.env_vars)
        # self.command = PrintSQLToConsoleCommand(
        #     env_vars=self.env_vars,
        #     context_builder=self.context_builder,
        #     run_on_db=False,
        # )
        # return CommandTestFactory(print_to_console_command=self.command)
