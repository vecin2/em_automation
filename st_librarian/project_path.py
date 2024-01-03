from pathlib import Path


class ProjectPath(object):
    def __init__(self, project_name):
        self.project_name = project_name

    def absolute(self, project_relative_path):
        parent_folder = Path(__file__).parent  # parent folder of current file
        current = parent_folder
        while str(current) != str(current.root) and current.name != self.project_name:
            current = current.parent

        if current.name == self.project_name:
            return current / project_relative_path
        else:
            raise ValueError(
                f"Project name is set to {self.project_name}, but no parent folders with that name where found on the current stored location {parent_folder}"
            )
