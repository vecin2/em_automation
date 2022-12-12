from pathlib import Path

from sql_gen.commands.test_sql_file import TestSQLFile
from sql_gen.docugen.template_filler import TemplateFiller
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv
from sql_gen.ui import MenuOption, select_option


class TemplateSelectorDisplayer(object):
    def ask_for_template(self, options, default=""):
        text = "\nStart typing the template name('x' - Save && Exit): "
        return select_option(text, options, 10, default)


class TemplateSelector(object):
    def __init__(self, templates_path):
        self.templates_path = templates_path
        self.loader = SelectTemplateLoader(self.templates_path)
        self.displayer = TemplateSelectorDisplayer()

    def select_template(self, template_name=None, default=None):
        if not template_name:
            options = self.loader.list_options()
            option = self.displayer.ask_for_template(options, default=default)
            if option.code == "x":
                return None
            elif option.is_help:
                self.show_help(option.name)
                return self.select_template(default=str(option))

            template_name = option.name
        return self.loader.load_template(template_name)

    def show_help(self, template_name):
        test_file = self.loader.load_test(template_name)
        if test_file:
            print(test_file.content)
        else:
            print(
                "No help defined for this template. You can define help by creating a test file under 'test_templates' folder"
            )
        # testfile = self.test_loader.load_test(self.test_name)


class SelectTemplateLoader(object):
    def __init__(self, templates_path):
        self.environment = EMTemplatesEnv().make_env(templates_path)

    def load_template(self, name):
        return self.environment.get_template(name)

    def load_test(self, name):
        root_templates = Path(self.environment.loader.searchpath[0])
        relative_template_path = Path(name)
        test_name = "test_" + relative_template_path.name
        relative_test_path = relative_template_path.parent / test_name
        absolute_test_path = (
            root_templates.parent / "test_templates" / relative_test_path
        )
        if absolute_test_path.exists():
            return TestSQLFile(absolute_test_path)
        return None

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
