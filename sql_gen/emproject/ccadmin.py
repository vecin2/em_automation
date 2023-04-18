import os
from pathlib import Path
from platform import uname

import sql_gen
from sql_gen import logger
from sql_gen.exceptions import CCAdminException


class CCAdmin(object):
    show_config_content = ""

    def __init__(self, root):
        self.root = root

    def show_config(self, params):
        sql_gen.logger.debug("Running ccadmin show-config " + params)
        result = self._run_ccadmin("show-config " + params)
        sql_gen.logger.debug("End Running ccadmin show-config")
        return result

    def generate_config(self):
        self.show_config("-Dformat=txt")


    def _run_ccadmin(self, command_and_args):
        ccadmin_path = Path(self._ccadmin_file())
        os.chdir(self.root)
        command = ("./" if self.in_wsl() else "") + ccadmin_path.name

        result = os.system(command + " " + command_and_args)
        if result == 0:
            return result
        raise CCAdminException(
            "Failed when running '"
            + command
            + " "
            + command_and_args
            + "' from "
            + os.getcwd()
        )

    def _ccadmin_file(self):
        ccadmin_file_name = "ccadmin." + self._ccadmin_file_ext()
        ccadmin_path = os.path.join(self.root, ccadmin_file_name)
        logger.debug("ccadmin found under: " + ccadmin_path)
        return ccadmin_path

    def _ccadmin_file_ext(self):
        logger.debug("Checking OS name: " + os.name)
        if os.name == "nt" or self.in_wsl():
            return "bat"
        else:
            return "sh"

    def in_wsl(self) -> bool:
        return "microsoft-standard" in uname().release
