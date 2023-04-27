from sqltask.test.utils.app_runner import ApplicationRunner


class InitAppRunner(ApplicationRunner):
    def __init__(self):
        super().__init__()

    def run(self, app=None):
        self._run([".", "init"], app=app)
        return self
