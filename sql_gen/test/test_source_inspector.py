import inspect
import sql_gen.test.utils.package_example as package_example
import sql_gen.test.utils.package_example.module_example as module_example
from sql_gen.test.utils.package_example.module_example import (
    example_filter1 as example_filter1,
)
from sql_gen.test.utils.package_example.module_example2 import (
    example_filter2 as example_filter2,
)
import sql_gen.docugen.source_inspector as source_inspector
import pkgutil


def test_extract_function_from_module():
    all_functions = inspect.getmembers(module_example, inspect.isfunction)
    title_function_name = all_functions[0][0]
    title_function = all_functions[0][1]
    assert "example_filter1" == title_function_name
    assert "Example1: hello" == title_function("hello")


def test_environment_contains_all_functions_defined_in_globals_module():
    globals = source_inspector.extract_module_functions(module_example)

    assert module_example.returns_string_passed == globals["returns_string_passed"]
    assert module_example.title_string == globals["title_string"]


def test_get_modules_import_path_from_package():
    modules = []
    package_path = package_example.__path__
    prefix = package_example.__name__ + "."
    for _, name, _ in pkgutil.iter_modules(package_path, prefix):
        modules.append(name)

    assert "sql_gen.test.utils.package_example.module_example" == modules[0]
    assert "sql_gen.test.utils.package_example.module_example2" == modules[1]


def test_environment_contains_all_filters_defined_in_filters_module():
    filters = source_inspector.extract_pkg_funcs_list_by_name(
        package_example, "get_template_filter"
    )

    assert example_filter1 == filters["example_filter1"]
    assert example_filter2 == filters["example_filter2"]
