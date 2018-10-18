import pytest
from sql_gen.sql_gen.prompter import Prompter
from jinja2 import DictLoader,Environment
from sql_gen.sql_gen.environment_selection import populate_filters

def run_with_multiple_templates(display_msgs,templates):
    env = Environment(
        loader=DictLoader(templates))
    populate_filters(env)
    prompter = Prompter(env)
    prompts = prompter.get_template_prompts(next(iter(templates)))
    assert_equals_prompt_text_list(display_msgs, prompts)

def run_with_one_template(display_msgs, template_text):
    templates={'one_template':template_text}
    run_with_multiple_templates(display_msgs, templates)

def assert_equals_prompt_text_list(questions, prompts):
    assert len(questions) == len(prompts)
    counter =0
    for key in prompts:
        assert_equal_prompt_text(questions[counter],prompts[key])
        counter+=1

def assert_equal_prompt_text(expected_text, prompt):
    assert expected_text+ ": " == prompt.get_diplay_text()

def test_no_vars_prompts_nothing():
    run_with_one_template([],
                 "Hello World!")

def test_var_prompts_var_name():
    run_with_one_template(['name'],
                 "Hello {{name}}!")

def test_default_displays_default_value(): 
    run_with_one_template(["name (default is Mundo)"],
                 "Hello {{ name | default ('Mundo') }}!")

def test_description_prompts_description_intead_of_var_name():
    template_text="Hello {{ name | description ('customer name') }}"
    display_msgs=['customer name']
    run_with_one_template(display_msgs, template_text)

def test_pipe_default_descripion_filters():
    template_text="Hello {{ prename }} {{ name | description ('World in english') | default ('Mundo')}}!"
    display_msgs=["prename","World in english (default is Mundo)"]
    run_with_one_template(display_msgs, template_text)

def test_duplicate_var_name_prompts_only_once_and_it_uses_first_one():
    template_text='Hola {{name | default("Marco")}}!,  {{name}}'
    display_msgs=['name (default is Marco)']
    run_with_one_template(display_msgs, template_text)

def test_should_not_prompt_var_which_has_value_assigned():
    template_text= "{% set process_descriptor_ref_id = process_descriptor_id %}"
    display_msgs=["process_descriptor_id"]
    run_with_one_template(display_msgs, template_text)

def test_prompts_var_passed_to_global_function():
    template_text="{% set name = camel(a_var)%}"
    display_msgs=["a_var"]
    run_with_one_template(display_msgs, template_text)

def test_include_should_prompt_vars_from_included_template_in_order():
    templates={
     "main_template" : "{% include 'hello_world' %}.  I am Juan {{last_name}}",
     "hello_world"   : "Hello {{ name }}!"
     }
    display_msgs=["name","last_name"]
    run_with_multiple_templates(display_msgs,templates)

def test_should_not_prompt_var_which_is_set_within_included_template():
    templates={
     "main_template" : "{% include 'set_name' %}.  I am Juan {{last_name}}",
     "set_name"      : "{% set name = 'Juan' %}!"
     }
    display_msgs=["last_name"]
    run_with_multiple_templates(display_msgs,templates)
