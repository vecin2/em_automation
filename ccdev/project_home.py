import os

import sql_gen
from sql_gen.exceptions import EnvVarNotFoundException

ENV_VAR_NAME = "EM_CORE_HOME"


class ProjectHome:
    def __init__(self, cwd, env_vars):
        self.cwd = cwd
        self.env_vars = env_vars

    def path(self):
        return self._emproject_home()

    def _emproject_home(self):
        try:
            return self._get_prj_home()
        except Exception as excinfo:
            sql_gen.logger.error(str(excinfo))
            raise excinfo

    def _get_prj_home(self):
        result = self._current_prj_path()

        if not os.path.exists(result):
            error_msg = (
                "Environment variable '"
                + ENV_VAR_NAME
                + "' exists "
                + "but it points to an invalid path"
            )
            raise ValueError(error_msg)

        return result

    def _current_prj_path(self):
        em_root = self._get_em_root_from_cwd()

        if em_root:
            return em_root
        elif ENV_VAR_NAME not in self.env_vars:
            help_text = "It should contain the path of your current EM project."
            raise EnvVarNotFoundException(ENV_VAR_NAME, help_text)

        return self.env_vars[ENV_VAR_NAME]

    def _get_em_root_from_cwd(self):
        return self._get_em_root_from_path(self.cwd)

    def _get_em_root_from_path(self, path):
        if self._is_em_root(path):
            return path
        parent = os.path.abspath(os.path.join(path, os.pardir))

        if parent == path:
            return ""

        return self._get_em_root_from_path(parent)

    def _is_em_root(self, path):
        return (
            os.path.exists(os.path.join(path, "bin"))
            and os.path.exists(os.path.join(path, "config"))
            and os.path.exists(os.path.join(path, "components"))
            and os.path.exists(os.path.join(path, "repository"))
        )
