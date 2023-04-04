from enum import Enum

from sql_gen.ui import prompt_suggestions


class HandlerType(Enum):
    RENDER = 1
    EXIT = 2
    VIEW_TEST = 3


class InputParser(object):

    def parse(self, input_str, option_list):
        str_option, params = self.split(input_str)
        option = self._matches_any(str_option, option_list)

        if not option or params:
            return None
        return MainMenuInput(option, params)
        # elif params and params == "-t":
        #     event_type = HandlerType.VIEW_TEST

    def _matches_any(self, option_entered, option_list):
        for option in option_list:
            if option.matches(option_entered):
                return option
        return None

    def split(self, input_str):
        input_arr = input_str.split("-", maxsplit=1)
        if len(input_arr) == 1:
            return input_arr[0].strip(), None

        return input_arr[0].strip(), "-" + input_arr[1].strip()


class MainMenuInput(object):
    def __init__(self, option, params):
        self.option = option
        self.params = params


class MainMenuDisplayer(object):
    def ask_for_input(self, options=None, default=None):
        text = "\nStart typing the template name('x' - Save && Exit): "

        return prompt_suggestions(text, options, default)


class MainMenu(object):
    def __init__(
        self,
        displayer=None,
        options=[],
        input_event_parser=None,
        handler=None,
        max_no_trials=10,
    ):
        self.displayer = displayer
        self.input_event_parser = input_event_parser
        self.handler = handler
        self.options = options
        saveAndExit = MenuOption.saveAndExit()
        self.options.append(saveAndExit)
        self.default_selection = ""
        self.exit = False
        self.max_no_trials = max_no_trials

    def run(self):
        while True:
            input = self.ask_for_input_until_valid()
            self.handler.handle(input, self)
            if self.exit:
                break

    def ask_for_input_until_valid(self):
        trial = 0
        input = None
        while trial <= self.max_no_trials:
            trial += 1
            input_str = self.displayer.ask_for_input(
                options=self.options, default=self.default_selection
            )
            input = self.input_event_parser.parse(input_str, self.options)
            if input:
                return input

        raise ValueError("Attempts to select a valid option exceeded.")


class MainMenuHandler(object):
    def __init__(self, handlers):
        self.handlers = handlers

    def handle(self, event, main_menu):
        for handler in self.handlers:
            if handler.handle(event, main_menu):
                break


class AbstractEventHandler(object):
    def handle(self, input, main_menu):
        if self.handles(input):
            self._do_handle(input.option, main_menu)
            return True
        else:
            return False

    def handles(self):
        """method to be implemented in child classes"""
        return None

    def type(self):
        """method to be implemented in child classes"""
        return None

    def _do_handle(self):
        """method to be implemented in child classes"""
        return None


class ExitHandler(AbstractEventHandler):
    def type(self):
        return HandlerType.EXIT

    def handles(self, input):
        return input.option.code == "x"

    def _do_handle(self, option, main_menu):
        main_menu.exit = True
        return True


class MenuOption(object):
    def __init__(self, code, name, info=False):
        self.code = code
        self.name = name
        self.info = info

    @staticmethod
    def saveAndExit():
        return MenuOption("x", "Save && Exit")

    @staticmethod
    def to_options(names):
        template_option_list = []
        for counter, name in enumerate(names):
            template_option = MenuOption(counter + 1, name)
            template_option_list.append(template_option)
        return template_option_list

    def matches(self, input_entered):
        if (
            self.code == input_entered
            or self.name == input_entered
            or input_entered == str(self)
        ):
            return True
        return False

    def __repr__(self):
        return str(self.code) + ". " + self.name

    def __eq__(self, other):
        return (
            self.code == other.code
            and self.name == other.name
            and self.info == other.info
        )