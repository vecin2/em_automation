import pyperclip
from rich.console import Console
from rich.syntax import Syntax

from sqltask.database.sql_runner import (RollbackTransactionExitListener,
                                         SQLRunner)
from sqltask.docugen.template_filler import TemplateFiller
from sqltask.shell.prompt import (ActionRegistry, Editor, EditTemplateAction,
                                  ExitAction, InteractiveTaskFinder,
                                  ProcessTemplateAction, RenderTemplateAction,
                                  ViewTemplateDocsAction,
                                  ViewTemplateInfoAction)
from sqltask.sqltask_jinja.context import ContextBuilder
from sqltask.sqltask_jinja.sqltask_env import EMTemplatesEnv
from sqltask.ui.sql_styler import SQLStyler


class PrintSQLToConsoleDisplayer(object):
    """Prints to console the command output"""

    def __init__(self):
        self.rendered_sql = ""

    def write(self, content, template=None):
        self.render_sql(content)

    def render_sql(self, sql_to_render):
        print("\n")
        syntax = Syntax(
            sql_to_render, "sql", theme="monokai", line_numbers=False, word_wrap=True
        )
        console = Console()
        console.print(syntax)
        print("\n")
        self._append_rendered_text(sql_to_render)

    def _append_rendered_text(self, text):
        if self.rendered_sql != "" and text != "":
            self.rendered_sql += "\n"
        self.rendered_sql += text

    def current_text(self):
        return self.rendered_text


class ClipboardCopier:
    def __init__(self):
        self.styler = SQLStyler()

    def write(self, content, template=None):
        return self.styler.append_sql(content)

    def on_finish(self):
        return pyperclip.copy(self.styler.text())


class ShellBuilder:
    def __init__(self):
        self._project = None
        self._displayer = None

    def build(self):
        return ShellFactory(self._project, self._displayer).make_sqltask_shell()

    def project(self, project):
        self._project = project
        return self

    def displayer(self, displayer):
        self._displayer = displayer
        return self


class ShellFactory:
    def __init__(self, project=None, displayer=None):
        self.project = project
        self.displayer = displayer

    def make_sqltask_shell(self):
        return InteractiveTaskFinder(self._make_actions_registry())

    def _make_actions_registry(self):
        registry = ActionRegistry()
        sql_runner = SQLRunner(self.project.db)
        clipboard_copier = ClipboardCopier()

        registry.register(
            self.make_process_template_action(sql_runner, clipboard_copier)
        )
        registry.register(self.make_exit_action(sql_runner, clipboard_copier))

        return registry

    def make_process_template_action(self, sql_runner, clipboard_copier):
        library = self.project.library()

        loader = EMTemplatesEnv(library)
        process_template_action = ProcessTemplateAction(
            loader,
            self.make_render_template_action(
                library, sql_runner, clipboard_copier, loader
            ),
        )
        editor_cmd = self.get_editor_cmd()
        if editor_cmd:
            process_template_action.register(
                "--edit", self.make_edit_template_action(library, editor_cmd)
            )
        process_template_action.register("--info", ViewTemplateInfoAction(library))
        process_template_action.register("--docs", ViewTemplateDocsAction(library))
        return process_template_action

    def get_editor_cmd(self):
        if "edit.template.cmd" in self.project.merged_config():
            return self.project.merged_config()["edit.template.cmd"]
        return None

    def make_edit_template_action(self, library, editor_cmd):
        return EditTemplateAction(library, self.make_editor(editor_cmd))

    def make_editor(self, editor_cmd):
        path_converter = (
            self.project.merged_config()["editor.path.converter"]
            if "editor.path.converter" in self.project.merged_config()
            else None
        )
        return Editor(editor_cmd, path_converter)

    def make_render_template_action(
        self, library, sql_runner, clipboard_copier, loader
    ):
        context_builder = ContextBuilder(self.project)
        context = context_builder.build()
        template_filler = TemplateFiller(initial_context=context)
        template_filler.append_listener(sql_runner)
        template_filler.append_listener(self.displayer)
        template_filler.append_listener(clipboard_copier)
        return RenderTemplateAction(template_filler, loader)

    def make_exit_action(self, sql_runner, clipboard_copier):
        exit_action = ExitAction()
        exit_action.append_listener(self.make_transaction_decorator(sql_runner))
        exit_action.append_listener(clipboard_copier)
        return exit_action

    def make_transaction_decorator(self, sql_runner):
        return RollbackTransactionExitListener(sql_runner)
