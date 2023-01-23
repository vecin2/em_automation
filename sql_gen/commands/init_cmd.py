class InitCommand(object):
    def __init__(self, app_project):
        self.app_project = app_project

    def run(self):
        print("Im running init")
        core_properties_path = self.app_project.paths["core_config"].path
        with open(core_properties_path, "+w") as f:
            f.write("somethign")
