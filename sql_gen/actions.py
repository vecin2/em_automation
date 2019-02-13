from sql_gen.docugen.template_filler import TemplateFiller
class ExitAction():
    """Does nothing and exits"""
    def run(self):
        return ""

class FillTemplateAction():
    """It fills the template values"""
    def __init__(self,template_name, loader,template_filler=TemplateFiller()):
        self.template_name =template_name
        self.loader = loader
        self.template_filler =template_filler
    def run(self):
        template = self.loader.get_template(self.template_name)
        return self.template_filler.fill(template,{})

