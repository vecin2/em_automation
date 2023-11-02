from sqltask.docugen.render_template_handler import RenderTemplateHandler
from sqltask.docugen.template_filler import TemplateFiller
from sqltask.main_menu import (InputParser, MainMenu, MainMenuDisplayer,
                               MainMenuHandler)


class RendererBuilder(object):
    def __init__(self):
        self.listeners = []
        # self.context_builder = None
        self.context = None
        self.loader = None

    def append_listener(self, listener):
        self.listeners.append(listener)
        return self

    def with_loader(self, loader):
        self.loader = loader

    def build(self):
        template_renderer = TemplateFiller(initial_context=self.get_context())
        for listener in self.listeners:
            template_renderer.append_listener(listener)
        render_template_handler = RenderTemplateHandler(
            template_renderer,
            loader=self.loader,
        )
        return render_template_handler

    def with_context(self, context):
        self.context = context

    def get_context(self):
        if not self.context:
            self.context = self.context_builder.build()
        return self.context


class MainMenuBuilder(object):
    def __init__(self):
        self.template_renderer_listeners = []
        self.loader = None
        self.context_builder = None
        self.context = None
        self.exit_handler_listener = None
        # self.renderer_builder = RendererBuilder()
        self.options = None
        self.handlers = []

    @staticmethod
    def base_setup(project, templates_path):
        builder = MainMenuBuilder()
        return builder

    def register_render_listener(self, listener):
        self.renderer_builder.append_listener(listener)
        return self

    def get_context(self):
        if not self.context:
            self.context = self.context_builder.build()
        return self.context

    def with_loader(self, loader):
        self.loader = loader

    def get_exit_listeners(self, listener):
        self.exit_handler_listener = listener

    def append_handler(self, handler):
        self.handlers.append(handler)

    def build(self):
        menu_handler = MainMenuHandler(self.handlers)

        displayer = MainMenuDisplayer()
        return MainMenu(
            displayer=displayer,
            options=self.options,
            input_event_parser=InputParser(),
            handler=menu_handler,
            max_no_trials=10,
        )
