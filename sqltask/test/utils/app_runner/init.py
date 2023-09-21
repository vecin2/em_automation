from sqltask.test.utils.app_runner import ApplicationRunner


class InitAppRunner(ApplicationRunner):
    def __init__(self):
        super().__init__()

    def run(self):
        self._run([".", "init"])
        return self

    def confirm_save(self):
        self.user_inputs("y")
        return self

    def with_properties(self, properties):
        for k, v in properties.items():
            self.user_inputs(v)
        return self
