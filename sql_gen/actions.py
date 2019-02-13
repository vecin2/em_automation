from sql_gen.docugen.template_renderer import TemplateRenderer
class ExitAction():
    """Does nothing and exits"""
    def run(self):
        return ""

class FillTemplateAction():
    """It fills the template values"""
    def __init__(self,template_name, loader):
        self.template_name =template_name
        self.loader = loader
    def run(self):
        template = self.loader.get_template(self.template_name)
        return TemplateRenderer(None,None).fill_template(template,{})

