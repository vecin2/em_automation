from sql_gen.docugen.template_filler import TemplateFiller
class ExitAction():
    """Does nothing and exits"""
    def run(self):
        return ""

class FillTemplateAction():
    """It fills the template values"""
    def __init__(self,template_name, loader,initial_context={}):
        self.template_name =template_name
        self.loader = loader
        self.template_filler = TemplateFiller()
        self.initial_context = initial_context
    def run(self):
        template = self.loader.get_template(self.template_name)
        #pass a copy of the intial context otherwise if we run the same
        #action twice the second time the context is already populated
        return self.template_filler.fill(template,
                                         dict(self.initial_context))

