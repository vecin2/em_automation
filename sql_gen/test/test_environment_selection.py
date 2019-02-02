from sql_gen.docugen.env_builder import EnvBuilder
from sql_gen.docugen.environment_selection import TemplateSelector,TemplateOption
import pytest

class FakeTemplateSelectorDisplayer(object):
    def display(self,options):
        self.last_rendered =str(options)


def test_display_options(fs):
    templates_path="/opt/sqltask/templates"
    fs.create_file(templates_path+"/menu/template_one.sql")
    em_env = EnvBuilder().set_fs_path(templates_path).build()
    displayer=FakeTemplateSelectorDisplayer()

    template_selector = TemplateSelector(em_env,displayer)
    template_selector.show_options()

    option_one = TemplateOption(0,"template_one.sql")
    assert str([option_one]) == displayer.last_rendered

def test_sql_template_path_set_non_existing_folder_returns_0(fs):
    templates_path="/opt/sqltask/templates"
    em_env = EnvBuilder().set_fs_path(templates_path).build()
    displayer=FakeTemplateSelectorDisplayer()

    template_selector = TemplateSelector(em_env,displayer)
    template_selector.show_options()

    assert str([]) == displayer.last_rendered

