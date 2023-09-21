import os

# from sqltask.docugen.completer import PathCompleter
from prompt_toolkit.completion.filesystem import PathCompleter
from sqltask.sqltask_jinja.filters import PromptFilter


def filepath(value):
    return value


def get_template_filter():
    return filepath


class FilepathFilter(PromptFilter):
    def __init__(self, jinja_filter, env_vars=os.environ):
        self.filter = jinja_filter

    def apply(self, prompt, context):
        get_paths_func = lambda: ["/"]
        prompt.completer = PathCompleter(get_paths=get_paths_func)
