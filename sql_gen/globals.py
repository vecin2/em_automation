from sql_gen.current_project import app
import pymssql
import sys
from sql_gen.queries.queries import Keynames
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit import prompt

def camelcase(st):
    if not st:
        return ""
    output = ''.join(x for x in st.title() if x.isalnum())
    return output[0].lower() + output[1:]

def prj_prefix():
    return app.emproject.prefix()

