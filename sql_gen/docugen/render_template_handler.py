from sql_gen.main_menu import AbstractEventHandler, HandlerType


class RenderTemplateHandler(AbstractEventHandler):
    def __init__(
        self, template_renderer, loader=None, initial_context=None, listener=None
    ):
        self.template_renderer = template_renderer
        self.loader = loader
        self.initial_context = initial_context
        self.listener = listener

    def type(self):
        return HandlerType.RENDER

    def handles(self, input):
        #only exit and template options this is good enough for now
        #in future might need to check if loader can load template
        return input.option.code != "x"

    def _do_handle(self, option, main_menu):
        template = self.loader.get_template(option.name)
        rendered_text = self.template_renderer.fillAndRender(
            template, self.initial_context
        )
        self.listener.write(rendered_text, template)
        return True
