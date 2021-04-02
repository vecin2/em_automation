import os
from sql_gen.exceptions import InvalidFileSystemPathException


class Path(object):
    def __init__(self, path=""):
        self.path = path

    def exists(self):
        return os.path.exists(self.path)

    def listdir(self):
        if not self.exists() or not os.listdir(self.path):
            return []
        # if there is at least one module created
        return [
            name
            for name in os.listdir(self.path)
            if os.path.isdir(os.path.join(self.path, name))
        ]

    def join(self, str_path):
        return Path(os.path.join(self.path, str_path))


class ProjectLayout(dict):
    def __init__(self, root, paths, mandatory_keys=[]):
        self.root = root
        self.paths = paths
        self.mandatory_keys = mandatory_keys

    def __getitem__(self, key):
        return Path(os.path.join(self.root, self.paths[key]))

    def check(self):
        for key in self.paths:
            self.check_path(key)

    def check_path(self, key):
        path = self.paths[key]
        if self.is_mandatory(key) and not self.exists(key):
            raise InvalidFileSystemPathException(
                "Path '" + self[key].path + "' does not exist."
            )

    def is_mandatory(self, key):
        return key in self.mandatory_keys

    def path(self, key):
        full_path = os.path.join(self.root, self[key])
        return Path(full_path)

    def exists(self, key):
        return self[key].exists()

    def listdir(self, key):
        return self.paths[key].listdir()
