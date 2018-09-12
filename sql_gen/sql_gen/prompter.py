from jinja2 import meta


class Prompter(object):
    def __init__(self, env):
        self.env = env

    def get_prompts(self, template_source_text):
        result=[]
        ast = self.env.parse(template_source_text)
        template_source = TemplateSource(template_source_text,self.env)
        for undeclared_var in template_source.get_ordered_undefined_variables():
            result.append(Prompt(undeclared_var,template_source.get_filters(undeclared_var)))
        return result

    def get_template_prompts(self, template_name):
        from sql_gen.sql_gen.template_source import TemplateSource
        result=[]
        template_source_text = self.env.loader.get_source(self.env,template_name)[0]
        template_source = TemplateSource(template_name,self.env)
        return template_source.get_prompts()

    def __get_ordered_undefined_variables(self, template_source_text,ast):
        undeclare_variables = meta.find_undeclared_variables(ast)
        list_a = template_source_text.split()
        return sorted(undeclare_variables, key=lambda x: list_a.index(x))


    def build_context(self):
        prompts = self.get_prompts()
        context ={}

        for prompt in prompts:
            prompt.populate_value(context)
        return context

class Prompt:
    def __init__(self, variable_name, filter_list):
        self.variable_name =variable_name
        self.filter_list = filter_list

    def get_diplay_text(self):
        self.display_text = self.variable_name
        for template_filter in self.filter_list:
            self.display_text = template_filter.apply(self.display_text);
        return self.display_text+": "

    def append_filter(self, prompt_filter):
        self.filter_list.append(prompt_filter)

    def populate_value(self,context):
        var =input(self.get_diplay_text())
        if var:
            context[self.variable_name] = var
