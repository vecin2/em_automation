from pathlib import Path

from sql_gen.commands.test_sql_file import TestSQLFile
from sql_gen.ui import MenuOption, select_option


class TemplateSelectorDisplayer(object):
    def ask_for_template(self, options, default=""):
        text = "\nStart typing the template name('x' - Save && Exit): "
        return select_option(text, options, 10, default)


class SelectTemplateLoader(object):
    def __init__(self, environment):
        self.environment = environment

    def load_template(self, name):
        return self.environment.get_template(name)

    def load_test(self, name):
        root_templates = Path(self.environment.loader.searchpath[0])
        relative_template_path = Path(name)
        test_name = "test_" + relative_template_path.name
        relative_test_path = relative_template_path.parent / test_name
        absolute_test_path = (
            root_templates.parent / "test_templates" / relative_test_path
        )
        if absolute_test_path.exists():
            return TestSQLFile(absolute_test_path)
        return None

    def list_options(self):
        saveAndExit = MenuOption("x", "Save && Exit")
        result = self._template_options()
        result.append(saveAndExit)
        return result

    def _template_options(self):
        template_names = self.environment.list_templates(
            None, self.list_templates_filter
        )
        return self._to_options(template_names)

    def list_templates_filter(self, template_name):
        if "hidden_templates" not in template_name:
            return True

    def _to_options(self, template_list):
        self.template_option_list = []
        for counter, template_path in enumerate(template_list):
            template_option = MenuOption(counter + 1, template_path)
            self.template_option_list.append(template_option)
        return self.template_option_list


class InteractiveTemplateSelector(object):
    def __init__(
        self,
        writer=None,
        initial_context={},
        selector=None,
        loader=None,
        parser=None,
        template_filler=None,
    ):
        self.writer = writer
        self.initial_context = initial_context
        self.loader = loader
        self.displayer = TemplateSelectorDisplayer()
        self.parser = parser
        self.template_filler = template_filler

    def run(self):
        template = self.select()
        while template:
            self.template_filler.set_template(template)
            filled_template = self.template_filler.fill(dict(self.initial_context))
            self.writer.write(filled_template, template)
            template = self.select()

    def select(self):
        return self.parse_option(self.prompt_template(self.loader.list_options()))

    def parse_option(self, option):
        return self.parser.parse(option)

    def prompt_template(self, options=None, default=None):
        return self.displayer.ask_for_template(options, default=default)


class ActionParser:
    def __init__(self, loader):
        self.loader = loader

    def parse(self, option):
        if option.code == "x":
            return None
        if option.is_help:
            self.show_help(option.name)
            return self.select(default=str(option))
        return self.loader.load_template(option.name)

    def show_help(self, template_name):
        test_file = self.loader.load_test(template_name)
        if test_file:
            print(test_file.content)
        else:
            print(
                "No help defined for this template. You can define help by creating a test file under 'test_templates' folder"
            )
        # testfile = self.test_loader.load_test(self.test_name)
