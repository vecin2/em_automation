import pytest
from sql_gen.commands.verify_templates_cmd import TestFileParser, PythonModuleTemplate


def test_parse_template_values():
    parser = TestFileParser()
    string = "--{'name':'Marlon'}\n" "hello Marlon!"
    values = parser.parse_values(string)
    assert {"name": "Marlon"} == values


def test_parse_empty_values_if_not_dictionary():
    parser = TestFileParser()
    string = "--{'name':'Marlon'}\n" "hello Marlon!"
    values = parser.parse_values(string)
    assert {"name": "Marlon"} == values


def test_parse_one_line_expected_sql():
    parser = TestFileParser()
    string = "hello Martin!"
    assert {} == parser.parse_values(string)
    assert "hello Martin!" == parser.parse_expected_sql(string)


def assert_equal_sql(expected, actual):
    assert expected == actual


def test_parse_multiple_lines_expected_sql():
    parser = TestFileParser()
    string = "--{'name':'Martin'}\n" "hello Martin!\n" "This is David"
    actual = parser.parse_expected_sql(string)
    assert_equal_sql("hello Martin!\nThis is David", actual)


source = PythonModuleTemplate()


def test_convert_one_line_str_to_source():
    string = "Hello Mark"
    assert string == eval(source.convert_to_src(string))


def test_convert_multiple_line_str_to_source():
    string = "Hello Mark\nHow are you?"
    assert string == eval(source.convert_to_src(string))


def test_convert_str_to_source_scapes_quotes():
    string = 'Hello "Animal"'
    assert string == eval(source.convert_to_src(string))
