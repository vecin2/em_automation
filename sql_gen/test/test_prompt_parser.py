from sql_gen.sql_gen.prompt_parser import PromptParser
from jinja2 import Template,Environment,DictLoader
from sql_gen.sql_gen.environment_selection import populate_filters_and_globals
import pytest

class TestPromptBuilder(object):
    def __init__(self, source):
        self.source = source
        self.templates = {"one_template":source}

    def _parser(self):
        self.template = self._template()
        return PromptParser(self.template)

    def _template(self):
        return self._env().get_template("one_template")

    def _env(self):
        env = Environment(
            loader=DictLoader(self.templates))
        populate_filters_and_globals(env)
        return env

    def and_template(self, template_name, source):
        self.templates[template_name]=source
        return self

    def with_values(self,template_values):
        self.template_values =template_values
        return self

    def should_prompt_next(self,msg):
        prompt = self._parser().next_prompt(self.template_values)
        self.assert_display_msg(msg, prompt)
        return self

    def should_suggest(self,suggestions):
        prompt = self._parser().next_prompt(self.template_values)
        assert suggestions == prompt.completer.suggestions
        return self

    def does_not_prompt(self):
        assert None == self._parser().next_prompt(self.template_values)

    def assert_display_msg(self,msg, prompt):
        assert msg +": " == prompt.get_display_text()


def template(source):
    return TestPromptBuilder(source)

def test_no_vars_prompts_nothing():
    template("Hello World").with_values({}).does_not_prompt()

def test_var_prompts_var_name():
    template("hello {{name}}").with_values({}).should_prompt_next("name")

def test_should_prompt_vars_until_all_values_are_filled():
    template("hello {{name}} {{last_name}}").with_values({})\
            .should_prompt_next("name")\
            .with_values({"name":"John"})\
            .should_prompt_next("last_name")\
            .with_values({"name":"John", "last_name":"Smith"})\
            .does_not_prompt()

def test_default_none_should_default_to_NULL():
    template("{{name | default (None)}}").with_values({})\
                                       .should_prompt_next("name (default is NULL)")

def test_default_zero_should_default_to_zero():
    template("{{name | default (0)}}").with_values({})\
                                       .should_prompt_next("name (default is 0)")

def test_default_displays_default_value():
    template("{{name | default ('World')}}").with_values({})\
                                       .should_prompt_next("name (default is World)")

def test_default_should_resolve_var():
    template("{% set my_name = 'David'%}{{ name | default(my_name)}}")\
            .with_values({})\
            .should_prompt_next("name (default is David)")

def test_default_should_resolve_dict():
    template("{%set dict = {'name':'Pedro'}%} {{name | default(dict['name'])}}")\
            .with_values({})\
            .should_prompt_next("name (default is Pedro)")

def test_default_throws_exception_if_parameter_is_a_function():
    with pytest.raises(ValueError) as e_info:
        template("{% set my_name = 'David'%}{{ name | default(camelcase('david'))}}")\
                .with_values({})\
                .should_prompt_next("")
    assert "Default Filters at the moment only support constant values" in str(e_info.value)

def test_description_prompts_description_intead_of_var_name():
    template("{{name | description ('Customer name')}}").with_values({})\
                                       .should_prompt_next("Customer name")
def test_descrioption_resolve_vars():
    template("{%set my_name = 'Victor'%}{{name | description(my_name)}}%}").with_values({})\
                                        .should_prompt_next("Victor")

def test_default_piped_with_description_then_desc_overrides_default():
    template("{{ name | default ('Mundo') | description ('World in english')}}").with_values({})\
                                       .should_prompt_next("World in english")

def test_pipe_descripion_default_filters():
    template("{{ name | description ('Customer name') | default ('John')}}").with_values({})\
                                       .should_prompt_next("Customer name (default is John)")

def test_duplicate_var_name_prompts_only_once_and_it_uses_first_one():
    template("{{ name | default ('John')}}, {{name}}").with_values({})\
                                       .should_prompt_next("name (default is John)")

def test_should_not_prompt_var_which_has_value_assigned():
    template("{% set process_descriptor_ref_id = process_descriptor_id %}").with_values({})\
                                       .should_prompt_next("process_descriptor_id")

def test_prompts_var_passed_to_global_function():
    template("{% set name = camelcase(a_var)%}").with_values({})\
                                       .should_prompt_next("a_var")

def test_include_should_prompt_vars_from_included_template_in_order():
    template("{% include 'hello_world' %}.  I am Juan {{last_name}}")\
            .and_template("hello_world","Hello {{name}}")\
            .with_values({})\
            .should_prompt_next("name")

def test_should_not_prompt_var_which_is_set_within_included_template():
    template("{% include 'set_name' %}. I am {{name}} {{last_name}}")\
            .and_template("set_name","{% set name = 'Juan' %}")\
            .with_values({})\
            .should_prompt_next("last_name")

def test_suggest_should_populate_prompt_suggestions():
    template("{{ name | suggest([1,2])}}")\
            .with_values({})\
            .should_prompt_next("name")\
            .should_suggest([1,2])

def test_suggest_should_resolve_vars():
    template("{% set suggestions = range(1,4)%}{{ name | suggest(suggestions)}}")\
            .with_values({})\
            .should_prompt_next("name")\
            .should_suggest([1,2,3])

