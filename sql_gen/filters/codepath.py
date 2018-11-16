from sql_gen.filters import PromptFilter
from sql_gen.sql_gen.completer import PathCompleter
from sql_gen.current_project import app
import os

def codepath(value):
    return value

def get_template_filter():
    return codepath

class CodepathFilter(PromptFilter):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter;

    def apply(self, prompt,context):
        project_modules= app.emproject.repo_modules_path()
        product_modules= app.emproject.product_prj().repo_modules_path()
        get_paths_func= (lambda:[ project_modules, product_modules])
        prompt.completer = PathCompleter(get_paths=get_paths_func)
