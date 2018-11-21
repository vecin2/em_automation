import inspect
import sql_gen.test.utils.package_example as package_example
import sql_gen.test.utils.package_example.module_example as module_example
from sql_gen.test.utils.package_example.module_example import example_filter1 as example_filter1

import sql_gen.test.utils.package_example.module_example2 as module_example2
from sql_gen.test.utils.package_example.module_example2 import example_filter2 as example_filter2

from sql_gen.sql_gen.environment_selection import populate_globals, populate_filters, EMTemplatesEnv,TemplateSelector,TemplateOption
from jinja2 import Environment
import pkgutil
import os
import pytest
@pytest.mark.skip
def test_template_folder():
    env_vars={"SQL_TEMPLATES_PATH":"/opt/sqltasktemplates"}
    env = EMTemplatesEnv().get_env(env_vars)
    assert "/opt/sqltasktemplates" ==env.loader.searchpath[0]

class FakeTemplateSelectorDisplayer(object):
    def display(self,options):
        self.last_rendered =str(options)

def test_display_options(fs):
    fs.create_file("opt/sqltask/templates/menu/template_one.sql")
    env_vars={"SQL_TEMPLATES_PATH":"/opt/sqltask/templates"}
    option_one = TemplateOption(0,"template_one.sql")

    displayer=FakeTemplateSelectorDisplayer()
    template_selector = TemplateSelector(env_vars,displayer)
    template_selector.show_options()
    assert str([option_one]) == displayer.last_rendered

def test_sql_template_path_not_set_computes_loc_from_em_core_home(fs):
    fs.create_file("opt/my_project/sqltask/templates/menu/template_one.sql")
    env_vars={"EM_CORE_HOME":"/opt/my_project"}
    option_one = TemplateOption(0,"template_one.sql")

    displayer=FakeTemplateSelectorDisplayer()
    template_selector = TemplateSelector(env_vars,displayer)
    template_selector.show_options()
    assert str([option_one]) == displayer.last_rendered

def test_sql_template_path_set_non_existing_folder_returns_0(fs):
    env_vars={"SQL_TEMPLATES_PATH":"/opt/sqltask/templates"}
    option_one = TemplateOption(0,"template_one.sql")

    displayer=FakeTemplateSelectorDisplayer()
    template_selector = TemplateSelector(env_vars,displayer)
    template_selector.show_options()
    assert str([]) == displayer.last_rendered

def test_extract_function_from_module():
    all_functions = inspect.getmembers(module_example, inspect.isfunction)
    title_function_name =all_functions[0][0]
    title_function =all_functions[0][1]
    assert "example_filter1" ==title_function_name
    assert "Example1: hello" == title_function("hello")

def test_it_uses_default_global_module_if_not_specified():
    env = Environment()
    populate_globals(env)
    assert "camelcase" in list(env.globals.keys())

def test_environment_contains_all_functions_defined_in_globals_module():
    env = Environment()

    populate_globals(env, module_example)

    assert module_example.returns_string_passed == env.globals['returns_string_passed']
    assert module_example.title_string == env.globals['title_string']

def test_get_modules_import_path_from_package():
    modules=[]
    package_path = package_example.__path__
    prefix = package_example.__name__+"."
    for _, name, _ in pkgutil.iter_modules(package_path, prefix):
        modules.append(name)

    assert "sql_gen.test.utils.package_example.module_example" == modules[0]
    assert "sql_gen.test.utils.package_example.module_example2" == modules[1]

def test_environment_contains_all_filters_defined_in_filters_module():
    env = Environment()
    populate_filters(env,package_example)

    assert example_filter1 ==  env.filters['example_filter1']
    assert example_filter2 ==  env.filters['example_filter2']

def test_it_uses_default_filters_package_if_not_specified():
    env = Environment()
    populate_filters(env)
    assert "description" in list(env.filters.keys())
