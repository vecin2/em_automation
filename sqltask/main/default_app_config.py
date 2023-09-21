from pathlib import Path

from sqltask.app_project import AppProject
from sqltask.log import log
from sqltask.main.command_factory import CommandFactory
from sqltask.main.command_line_app import CommandLineSQLTaskApp, SysArgParser
from sqltask.main.main_menu_builder import PrintSQLToConsoleDisplayer
from sqltask.main.project_home import ProjectHome


class DefaultAppContainer(object):
    def resolve(self, cwd, env_vars=None):
        project_home = ProjectHome(cwd, env_vars)
        project = AppProject(project_home.path())
        cwd_library = Path(cwd) / ".sqltask_library"
        if cwd_library.exists():
            project.set_library_path(Path(cwd_library.read_text().strip()))
        logger = self.setup_logger(project)
        self.console_printer = PrintSQLToConsoleDisplayer()
        command_factory = CommandFactory(project, self.console_printer)
        args_parser = SysArgParser(command_factory)
        application = CommandLineSQLTaskApp(project_home, args_parser, logger)
        return application

    def setup_logger(self, project):
        return LoggerConfigurator().setup_logger(project)


class LoggerConfigurator(object):
    def setup_logger(self, project):
        file = project.logging_config_file()
        if file:
            log.setup_from_file(file)
        else:
            logs_dir = project.sqltask_logs_dir()
            print("Default logs dir is: " + logs_dir)
            log.basic_setup(logs_dir=logs_dir)
        return log.logger
