from sql_gen.sql_gen.prompter import PromptVisitor
from jinja2 import Template
import pytest

t = Template("")
def parse(template_text):
    return  t.environment.parse(template_text)

def get_prompts(ast):
    return PromptVisitor(ast).visit(ast)

