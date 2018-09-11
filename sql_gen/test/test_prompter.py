from sql_gen.sql_gen.template_source import TemplateSource
from sql_gen.sql_gen.prompter import Prompter
import pytest
from test.util_test_template_env import test_env
import os
from jinja2 import Environment, meta, Template, nodes, FileSystemLoader, select_autoescape
from sql_gen.sql_gen.filter_loader import load_filters

env=test_env()
#dirname = os.path.dirname(__file__)
#templates_path = "./"+os.path.join(dirname, 'templates')
#env = Environment(
#loader=FileSystemLoader("/home/dgarcia/dev/python/em_automation/sql_gen/test/templates"),
#autoescape=select_autoescape(['html', 'xml']))
load_filters(env)
#print("**********************"+templates_path)
print("********************"+ str(env.list_templates(".sql")))
source = env.loader.get_source(env,"hello_world.sql")[0]
print("sdfjsdfsd")

def run_test(display_msgs, template_source_text):
    prompter = Prompter(env)
    prompts = prompter.get_prompts(template_source_text)
    assert_equals_prompt_text_list(display_msgs, prompts)

def assert_equals_prompt_text_list(questions, prompts):
    assert len(questions) == len(prompts)
    counter =0
    for question in questions:
        assert_equal_prompt_text(question,prompts[counter])
        counter+=1

def assert_equal_prompt_text(expected_text, prompt):
    assert expected_text+ ": " == prompt.get_diplay_text()

def test_default():
    run_test(["name (default is Mundo)"],
              "Hello {{ name | default ('Mundo') }}!")

def test_description():
    run_test(["customer name"],
              "Hello {{ name | description ('customer name') }}")


def test_pipe_default_descripion_filters():
    template_text = "Hello {{ prename }} {{ name | description ('World in english') | default ('Mundo')}}!"
    run_test(["prename","World in english (default is Mundo)"],
              template_text)

def test_get_description_value_when_multiple_vars():
    run_test(["prename","first name"],
              "Hello {{ prename }} {{ name | description ('first name') }}!")

@pytest.mark.skip
def test_include_should_prompt_vars_from_included_template():
    run_test(["name"],
              "{% include 'hello_world.sql' %}.  I am Juan")
