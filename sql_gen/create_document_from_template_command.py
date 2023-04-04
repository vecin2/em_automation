from pathlib import Path

from sql_gen.commands.test_sql_file import TestSQLFile
from sql_gen.ui import prompt_suggestions


class TemplateSelectorDisplayer(object):
    def ask_for_template(self, options, default=""):
        text = "\nStart typing the template name('x' - Save && Exit): "
        return prompt_suggestions(text, options, default)


class SelectTemplateLoader(object):
    def __init__(self, environment):
        self.environment = environment

    def load_template(self, name):
        return self.environment.get_template(name)

    def load_test(self, name):
        root_templates = Path(self.environment.loader().searchpath[0])
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
        """ result.append(saveAndExit) """
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


class TemplateAction(object):
    def __init__(self, template_path, info=None):
        self.template_path = template_path
        self.info = info

    def is_exit(self):
        return self.template_path == "Save && Exit"

    def is_help(self):
        return self.info == "_test"



class TemplateSelector(object):
    def __init__(self, generator, parser=None, loader=None):
        self.generator = generator
        self.parser = parser
        self.no_of_retrials = 10
        self.counter = 0
        self.default_selection = None
        self.loader = loader
        self._option_list = None
        self.user_input = None

    def select(self, default=None):
        return self.choose_action()
        template = self.parser.parse(action)
        if action.info == "_test":
            self.default_selection = str(action)
            """ return self.select(default=str(action)) """
        return template

    @property
    def option_list(self):
        if not self._option_list:
            self._option_list = self.loader.list_options()
        return self._option_list

    def choose_action(self):
        action = None
        while not self.trials_exceed():
            self.user_input = self.prompt_template()
            action = self.get_action()
            if action:
                return action
            self.add_trial()
        raise ValueError("Attempts to select a valid option exceeded.")

    def add_trial(self):
        self.counter += 1

    def trials_exceed(self):
        return self.counter >= self.no_of_retrials

    def parse(self, option):
        if option.info == "x":
            return None
        if option.info:
            self.show_help(option.template_path)
        return self.generator.loader.load_template(option.template_path)

    def prompt_template(self):
        return self.generator.displayer.ask_for_template(
            self.option_list, default=self.default_selection
        )

    def get_action(self):
        option_entered, suffix = self.parse_suffix(self.user_input, "_test")
        option = self.match_any(option_entered, self.option_list)
        if not option:
            return None
        return TemplateAction(option.name, info=suffix)

    def match_any(self, option_entered, option_list):
        for option in option_list:
            if option.matches(option_entered):
                return option
        return None

    def parse_suffix(self, input_entered, suffix):
        info = None
        if len(input_entered) > len(suffix) and input_entered[-len(suffix) :] == suffix:
            info = suffix
            # remove '_test' to match template name
            input_entered = input_entered[: -len(suffix)]
        else:
            info = False
        return input_entered, info

    def run(self, option):
        template = self.parser.parse(option)
        if option.info == "_test":
            return self.select(default=str(option))
        return template


class ActionParser:
    def __init__(self, loader):
        self.loader = loader

    def parse(self, option):
        if option.info == "x":
            return None
        if option.info:
            self.show_help(option.template_path)
        return self.loader.load_template(option.template_path)

    def show_help(self, template_name):
        test_file = self.loader.load_test(template_name)
        if test_file:
            print(test_file.content)
        else:
            print(
                "No help defined for this template. You can define help by creating a test file under 'test_templates' folder"
            )


class InteractiveSQLGenerator(object):
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
        self.template_selector = TemplateSelector(
            self, parser=parser, loader=self.loader
        )

    def run(self):
        action = self.select()

        while not action.is_exit():
            if action.is_help():
                self.parser.show_help(action.template_path)
            else:
                self.render_template(action)
            action = self.select()

    def render_template(self, action):
        template = self.loader.load_template(action.template_path)
        """ self.template_filler.set_template(template) """
        filled_template = self.template_filler.fillAndRender(template,self.initial_context)
        self.writer.write(filled_template, template)

    def select(self, default=None):
        return self.template_selector.select(default)
