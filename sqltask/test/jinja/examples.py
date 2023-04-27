from jinja2 import nodes, Template, Environment, FileSystemLoader
from jinja2.ext import Extension
import os


def pedro():
    return "Pedro Alvarez"


def test_globals():
    templates_path = os.environ["SQL_TEMPLATES_PATH"]
    env = Environment(loader=FileSystemLoader(templates_path))
    env.globals["camel"] = pedro
    t = env.from_string("{% set name = camel()%}Name is {{name}}")
    t = env.get_template("test_globals.sql")
    assert "Name is Pedro Alvarez" == t.render({})
