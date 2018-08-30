from jinja2 import Environment, meta, Template, nodes, FileSystemLoader, select_autoescape
from sql_gen.sql_gen.filter_loader import load_filters
import os

def test_env():
    dirname = os.path.dirname(__file__)
    templates_path = os.path.join(dirname, 'templates')
    env = Environment(
            loader=FileSystemLoader(templates_path),
            autoescape=select_autoescape(['html', 'xml']))
    load_filters(env)
    return env
