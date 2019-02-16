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
        self.template_filler = TemplateFiller()
        self.template = self.loader.get_template(self.template_name)
    def run(self,initial_context):
        #pass a copy of the intial context otherwise if we run the same
        #action twice the second time the context is already populated
        return self.template_filler.fill(self.template,
                                         dict(initial_context))

