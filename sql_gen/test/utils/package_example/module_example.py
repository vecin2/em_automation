def example_filter1(string):
    return "Example1: " + string


def get_template_filter():
    return example_filter1


def returns_string_passed(string):
    return string


def title_string(string):
    return string.title()
