from jinja2 import nodes,meta, Template
from jinja2.nodes import Name, Filter
import importlib
from jinja2.visitor import NodeTransformer,NodeVisitor
from sql_gen.sql_gen.prompter import Prompt

class TemplateSource(object):
    def __init__(self,template_name, env):
        t = self.__get_template_with_source(env, template_name)
        self.template_source_text = t.source
        self.ast = env.parse(self.template_source_text)
       # TreeDrawer().print_node(self.ast)
       # print("**********************************************")
        self.__set_parent(self.ast,None)
        TemplateJoiner(env).visit(self.ast)
       # TreeDrawer().print_node(self.ast)

    def __get_template_with_source(self, env, template_name):
        t = env.get_template(template_name)
        t.source = env.loader.get_source(env,template_name)[0]
        return t    

    def __set_parent(self, node,parent):
        node.parent = parent
        for child in node.iter_child_nodes():
            self.__set_parent(child, node)
        return

    def get_prompts(self):
        return PromptVisitor().visit(self.ast)

    def __get_undeclared_variables(self,prompts):
        result=[]
        for prompt in prompts:
            result.append(prompt.variable_name)
        return result
    def __get_display_text(self,prompts):
        result=[]
        for prompt in prompts:
            result.append(prompt.get_diplay_text())
        return result
    def __sort_by_order_of_appearance(self,prompts):
        undeclare_variables = self.__get_undeclared_variables(prompts)
        display_msgs = self.__get_display_text(prompts)
        list_a = self.template_source_text.split()
        print("*********** undeclare_variables"+ str(undeclare_variables))
        print("*********** display_msgs"+ str(display_msgs))
        #sorted_vars =sorted(undeclare_variables, key=lambda x: list_a.index(x))
        return self.__sort_prompts_by_var_names(prompts, list_a)

    def __sort_prompts_by_var_names(self, prompts, sorted_vars):
        result =[]
        dictionary = {}
        for prompt in prompts:
            dictionary[prompt.variable_name] = prompt
        for variable in sorted_vars:
            if dictionary.get(variable) is not None:
                result.append(dictionary[variable])

        return result

    def get_ordered_undefined_variables(self):
        undeclare_variables = meta.find_undeclared_variables(self.ast)
        list_a = self.template_source_text.split()
        return sorted(undeclare_variables, key=lambda x: list_a.index(x))

