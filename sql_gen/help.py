from sql_gen.main_menu import AbstractEventHandler, HandlerType


class DisplayTemplateTestHandler(AbstractEventHandler):
    def __init__(self, library):
        self.library = library

    def type(self):
        return HandlerType.DISPLAY_TEST

    def handles(self, input):
        return input.option and input.option.code != 'x' and input.params =="-t"

    def _do_handle(self, option, main_menu):
        template = self.loader.get_template(option.name)
        rendered_text = self.template_renderer.fill_and_render(template)
        self.listener.write(rendered_text, template)
        return True
