from sql_gen.main_menu import AbstractEventHandler, EventType


class RenderTemplateHandler(AbstractEventHandler):
    def __init__(
        self, template_renderer, loader=None, initial_context=None, listener=None
    ):
        self.template_renderer = template_renderer
        self.loader = loader
        self.initial_context = initial_context
        self.listener = listener

    def _handled_event_type(self):
        return EventType.RENDER

    def _do_handle(self, option, main_menu):
        template = self.loader.load_template(option.name)
        rendered_text = self.template_renderer.fillAndRender(
            template, self.initial_context
        )
        self.listener.write(rendered_text, template)
        return True
