from jinja2 import Environment, FileSystemLoader

from sql_gen.app_project import AppProject
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv
from sql_gen.sqltask_jinja.context import init
from sql_gen.ui import prompt, MenuOption, select_option
from sql_gen.docugen.template_filler import TemplateFiller
from sql_gen.database.sqlparser import SQLParser


class TemplateSelectorDisplayer(object):
    def ask_for_template(self, options):
        text = "\nStart typing the template name('x' - Save && Exit): "
        return select_option(text, options, 10)


class TemplateSelector(object):
    def __init__(self, templates_path):
        self.templates_path = templates_path
        self.loader = SelectTemplateLoader(self.templates_path)
        self.displayer = TemplateSelectorDisplayer()

    def select_template(self, template_name=None):
        if not template_name:
            options = self.loader.list_options()
            option = self.displayer.ask_for_template(options)
            if option.code == "x":
                return None
            template_name = option.name
        return self.loader.load_template(template_name)


class SelectTemplateLoader(object):
    def __init__(self, templates_path):
        self.environment = EMTemplatesEnv().make_env(templates_path)

    def load_template(self, name):
        return self.environment.get_template(name)

    def list_options(self):
        saveAndExit = MenuOption("x", "Save && Exit")
        result = self._template_options()
        result.append(saveAndExit)
        return result

    def _template_options(self):
        template_names = self.environment.list_templates(
            None, self.list_templates_filter
        )
        return self._to_options(template_names)

    def list_templates_filter(self, template_name):
        if "hidden_templates" not in template_name:
            return True

    def _to_options(self, template_list):
        self.template_option_list = []
        for counter, template_path in enumerate(template_list):
            template_option = MenuOption(counter + 1, template_path)
            self.template_option_list.append(template_option)
        return self.template_option_list


class FillTemplateCommandDisplayer(object):
    def display_loading_templates_from(self, templates_path):
        print("\nTemplates loaded from '" + templates_path + "'")


class CreateDocumentFromTemplateCommand(object):
    def __init__(
        self,
        templates_path,
        writer=None,
        initial_context={},
        template_name=None,
        run_once=False,
    ):
        self.templates_path = templates_path
        self.writer = writer
        self.initial_context = initial_context
        self.template_name = template_name
        self.run_once = run_once

    def run(self):
        self.selector = TemplateSelector(self.templates_path)
        FillTemplateCommandDisplayer().display_loading_templates_from(
            self.templates_path
        )
        template = self.selector.select_template(self.template_name)
        while template:
            filled_template = TemplateFiller(template).fill(dict(self.initial_context))
            self.writer.write(filled_template, template)
            if self.run_once:
                return
            template = self.selector.select_template()
