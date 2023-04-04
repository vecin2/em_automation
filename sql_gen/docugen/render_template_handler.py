from sql_gen.main_menu import AbstractEventHandler, HandlerType


class RenderTemplateHandler(AbstractEventHandler):
    def __init__(
        self, template_renderer, loader=None, listener=None
    ):
        self.template_renderer = template_renderer
        self.loader = loader
        self.listener = listener

    def type(self):
        return HandlerType.RENDER

    def handles(self, input):
        return input.option and input.option.code != "x" and not input.params

    def _do_handle(self, option, main_menu):
        template = self.loader.get_template(option.name)
        rendered_text = self.template_renderer.fill_and_render(
            template
        )
        self.listener.write(rendered_text, template)
        return True
