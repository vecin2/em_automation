from enum import Enum

from sql_gen.ui import prompt_suggestions


class EventType(Enum):
    RENDER = 1
    EXIT = 2
    VIEW_TEST = 3


class InputEventParser(object):
    def parse(self, input_str, option_list):
        str_option, params = self.split(input_str)
        option = self._matches_any(str_option, option_list)

        if not option:
            return None
        if not params:
            if option.code == "x":
                event_type = EventType.EXIT
            else:
                event_type = EventType.RENDER
        elif params and params == "-t":
            event_type = EventType.VIEW_TEST
        else:
            return None
        return InputEvent(option, event_type)

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


class InputEvent(object):
    def __init__(self, option, type):
        self.option = option
        self.type = type

    def __eq__(self, other):
        return self.option == other.option and self.type == other.type

    def __repr__(self):
        return (self.option or "") + " " + str(self.type)


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
        event_handler=None,
        max_no_trials=10,
    ):
        self.displayer = displayer
        self.input_event_parser = input_event_parser
        self.event_handler = event_handler
        self.options = options
        saveAndExit = MenuOption.saveAndExit()
        self.options.append(saveAndExit)
        self.default_selection = ""
        self.exit = False
        self.max_no_trials = max_no_trials

    def run(self):
        while True:
            event = self.ask_for_input_until_valid()
            self.event_handler.handle(event, self)
            if self.exit:
                break

    def ask_for_input_until_valid(self):
        trial = 0
        event = None
        while trial <= self.max_no_trials:
            trial += 1
            input_str = self.displayer.ask_for_input(
                options=self.options, default=self.default_selection
            )
            event = self.input_event_parser.parse(input_str, self.options)
            if event:
                return event

        raise ValueError("Attempts to select a valid option exceeded.")


class MainMenuHandler(object):
    def __init__(self, event_handlers):
        self.event_handlers = event_handlers

    def handle(self, event, main_menu):
        for handler in self.event_handlers:
            if handler.handle(event, main_menu):
                break


class AbstractEventHandler(object):
    def handle(self, event, main_menu):
        if event.type == self._handled_event_type():
            return self._do_handle(event.option, main_menu)
        else:
            return False

    def _handled_event_type(self):
        """method to be implemented in child classes"""
        return None

    def _do_handle(self):
        """method to be implemented in child classes"""
        return None


class ExitHandler(AbstractEventHandler):
    def _handled_event_type(self):
        return EventType.EXIT

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
