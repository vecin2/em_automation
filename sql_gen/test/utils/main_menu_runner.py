from sql_gen.main_menu import (AbstractEventHandler, EventType, ExitHandler,
                               InputEventParser, MainMenu, MainMenuHandler)


class MainMenuDisplayer(object):
    def __init__(self, mocked_selections=None):
        self.selections = mocked_selections
        self.counter = 0

    def append_selections(self, mocked_selections):
        if not self.selections:
            self.selections = []
        self.selections.extend(mocked_selections)

    def ask_for_input(self, options=None, default=None):
        result = self.selections[self.counter]
        self.counter += 1
        return result


class FakeTemplateHandler(AbstractEventHandler):
    def __init__(self):
        self.rendered_templates = []

    def _handled_event_type(self):
        return EventType.RENDER

    def _do_handle(self, template_path, main_menu):
        self.rendered_templates.append(template_path.name)
        return True


class MainMenuRunner(object):
    def __init__(self):
        """self.template_renderer = FakeTemplateRenderer()"""
        self.render_template_handler = FakeTemplateHandler()
        self.exit_handler = ExitHandler()
        self.displayer = MainMenuDisplayer()

        self.menu_handler = MainMenuHandler(
            [self.render_template_handler, self.exit_handler]
        )

        self.input_parser = InputEventParser()

        self.max_no_of_trials = 10

    def with_selections(self, selections):
        self.displayer.append_selections(selections)
        return self

    def rendered_templates(self):
        return self.render_template_handler.rendered_templates

    def with_max_no_of_trials(self, number):
        self.max_no_of_trials = number
        return self

    def with_options(self, options):
        self.options = options

    def run(self):
        self.main_menu = MainMenu(
            displayer=self.displayer,
            options=self.options,
            input_event_parser=self.input_parser,
            event_handler=self.menu_handler,
            max_no_trials=self.max_no_of_trials,
        )
        self.main_menu.run()
