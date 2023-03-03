import os

from sql_gen.create_document_from_template_command import (
    ActionParser, InteractiveTemplateSelector, SelectTemplateLoader)
from sql_gen.database.sqlparser import SQLParser
from sql_gen.docugen.template_filler import TemplateFiller
from sql_gen.exceptions import DatabaseError
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv


class PrintSQLToConsoleDisplayer(object):
    """Prints to console the command output"""

    def __init__(self):
        self.rendered_sql = ""

    def write(self, content, template=None):
        self.render_sql(content)

    def render_sql(self, sql_to_render):
        print("\n")
        print(sql_to_render)
        self._append_rendered_text(sql_to_render)

    def _append_rendered_text(self, text):
        if self.rendered_sql != "" and text != "":
            self.rendered_sql += "\n"
        self.rendered_sql += text

    def current_text(self):
        return self.rendered_text


class PrintSQLToConsoleCommand(object):
    """Command which generates a SQL script from a template and it prints the output to console"""

    def __init__(
        self,
        context_builder=None,
        emprj_path=None,
        templates_path=None,
        run_on_db=True,
        listener=None,
    ):
        self.templates_path = templates_path
        self.context_builder = context_builder
        self.context = None
        self.listener = listener
        # If we are printing two templates, running the sql
        # allow the second template to see the modification made
        # by the first template  (kenyames, entities inserted, etc)
        self.run_on_db = run_on_db

    def run(self):
        if not self.context:
            self.context = self.context_builder.build()

        self.console_printer = PrintSQLToConsoleDisplayer()
        loader = SelectTemplateLoader(EMTemplatesEnv(self.templates_path))
        template_filler = TemplateFiller()
        self.interactive_selector = InteractiveTemplateSelector(
            self,
            self.context,
            loader=loader,
            parser=ActionParser(loader),
            template_filler=template_filler,
        )
        self.interactive_selector.run()
        # pyperclip.copy(self.sql_printed())
        self.context["_database"].rollback()

    def write(self, content, template=None):
        self.console_printer.write(content)
        result = None
        if self.run_on_db and self._is_runnable_sql(template):
            try:
                result = self._run_content_on_db(content)
                self.context["_database"].clearcache()
            except (Exception, DatabaseError) as e:
                if input("Do you want to continue (Y/N)?") == "N":
                    raise e

        if self.listener:
            self.listener.on_written(content, template)
        return result

    def _run_content_on_db(self, content):
        stmt = SQLParser().parse_statements(content)[0]
        if stmt.startswith("SELECT"):
            return self._db().fetch(stmt)
        else:
            self._db().execute(content)
            return None

    def _db(self):
        return self.context_builder.build()["_database"]

    def _is_runnable_sql(self, template):
        extension = os.path.splitext(template.filename)[1]
        return extension == ".sql"

    def sql_printed(self):
        return self.console_printer.rendered_sql
