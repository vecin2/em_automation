import os

from sqltask import logger
from sqltask.app_project import AppProject
from sqltask.docugen.completer import PathCompleter
from sqltask.main.project_home import ProjectHome
from sqltask.sqltask_jinja.filters import PromptFilter


def codepath(value):
    return value


def get_template_filter():
    return codepath


class CodepathFilter(PromptFilter):
    def __init__(self, jinja_filter, env_vars=os.environ):
        self.filter = jinja_filter

    def apply(self, prompt, context):
        project_home = ProjectHome(os.getcwd(), os.environ)

        app = context._vars["_app"] #AppProject(emprj_path=project_home.path())
        logger.debug("Applying CodePath filter to project :" + str(app.emroot))
        project_modules = str(app.paths["repo_modules"])
        product_modules = str(app.product_layout()["repo_modules"])
        get_paths_func = lambda: [project_modules, product_modules]
        prompt.completer = PathCompleter(get_paths=get_paths_func)
