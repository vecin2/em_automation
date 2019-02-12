from sql_gen.create_sqltask_command import CreateSQLTaskCommand
from sql_gen.commands import PrintSQLToConsoleCommand,PrintSQLToConsoleDisplayer
from sql_gen.create_document_from_template_command import CreateDocumentFromTemplateCommand,TemplateSelector,TemplateFiller,SelectTemplateLoader,SelectTemplateDisplayer
import argparse

class CommandFactory(object):
    def make(self):
        args =self.parse_args()
        path = args.dir
        if path:
            return CreateSQLTaskCommand()
        else:
            return self.make_print_sql_to_console_command()
    def make_print_sql_to_console_command(self):
        return PrintSQLToConsoleCommand(
                    CreateDocumentFromTemplateCommand(
                            TemplateSelector(
                                    SelectTemplateLoader(),
                                    SelectTemplateDisplayer()),
                            TemplateFiller()),
                    self._make_print_to_console_displayer())
    def _make_print_to_console_displayer(self):
        return PrintSQLToConsoleDisplayer()

    def parse_args(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-d", "--dir", help="Its the directory where the sql task will be written to. Its a relative path from  $CORE_HOME to, e.g. modules/GSCCoreEntites...")
        return ap.parse_args()


