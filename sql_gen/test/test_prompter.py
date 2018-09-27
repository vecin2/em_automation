import pytest
from sql_gen.sql_gen.prompter import Prompter
from test.utils.util_test_template_env import test_env

env=test_env()
def pedro():
    return "Pedro Alvarez"
env.globals['camel']=pedro

def run_test_file(expected_msgs, template_name):
    prompter = Prompter(env)
    prompts = prompter.get_template_prompts(template_name+".sql")
    assert_equals_prompt_text_list(expected_msgs, prompts)


def assert_equals_prompt_text_list(questions, prompts):
    assert len(questions) == len(prompts)
    counter =0
    for key in prompts:
        assert_equal_prompt_text(questions[counter],prompts[key])
        counter+=1

def assert_equal_prompt_text(expected_text, prompt):
    assert expected_text+ ": " == prompt.get_diplay_text()

def test_duplicate_var_name_prompts_only_once_and_it_uses_first_one():
    run_test_file(["name (default is Marco)"],
              "duplicate_var_name")

def test_should_not_prompt_var_which_has_value_assigned():
    # {% set process_descriptor_ref_id = process_descriptor_id %}
    run_test_file(["process_descriptor_id"],
              "one_var_equal_to_other_var")

def test_default(): 
    run_test_file(["name (default is Mundo)"],
              "one_var_default_filter")
def test_description():
    run_test_file(["customer name"],
              "one_var_description_filter")

def test_does_not_prompt_globals():
    run_test_file([],
              "invoke_global")

def test_prompts_var_passed_global_callables():
    run_test_file(["a_var"],
              "invoke_global_with_vars")

def test_pipe_default_descripion_filters():
    run_test_file(["prename","World in english (default is Mundo)"],
              "pipe_description_default_filter")

def test_include_should_prompt_vars_from_included_template():
    run_test_file(["name"],
              "include_plus_data")

def test_include_should_prompt_vars_from_included_template_before_current_ones():
    run_test_file(["name","last_name"],
              "include_plus_var")
def test_include_should_prompt_vars_from_included_template_after_current_one():
    run_test_file(["last_name","name"],
              "var_plus_include")

def test_should_not_prompt_var_which_is_set_within_included_template():
    #{% include 'hello_world.sql' %}
    #{{last_name}}
    #{% set full_name = name + last_name %}
    #I {{full_name}}
    run_test_file(["name","last_name"],
              "include_reuse_var_value")

