import sql_gen
import os
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

    def _run_ccadmin(self, command_and_args):
        result = os.system(self._ccadmin_file() + " " + command_and_args)
        if result == 0:
            return result
        raise CCAdminException(
            "Failed when running '"
            + self._ccadmin_file()
            + " "
            + command_and_args
            + "'"
        )

    def _ccadmin_file(self):
        ccadmin_file_name = "ccadmin." + self._ccadmin_file_ext()
        ccadmin_path = os.path.join(self.root, ccadmin_file_name)
        logger.debug("ccadmin found under: " + ccadmin_path)
        return ccadmin_path

    def _ccadmin_file_ext(self):
        logger.debug("Checking OS name: " + os.name)
        if os.name == "nt":
            return "bat"
        else:
            return "sh"
