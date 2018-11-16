from sql_gen.sqltask_jinja.filters import PromptFilter
from sql_gen.sql_gen.completer import PathCompleter
from sql_gen.current_project import app
from sql_gen.logger import logger

def codepath(value):
    return value

def get_template_filter():
    return codepath

class CodepathFilter(PromptFilter):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter;

    def apply(self, prompt,context):
        logger.debug("Applying CodePath filter to project :"+app.emproject.root)
        project_modules= app.emproject.paths['repo_modules']
        product_modules= app.emproject.product_prj().paths['repo_modules']
        get_paths_func= (lambda:[ project_modules, product_modules])
        prompt.completer = PathCompleter(get_paths=get_paths_func)