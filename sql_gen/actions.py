from sql_gen.docugen.template_filler import TemplateFiller
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
        return TemplateFiller().fill(template,{})

