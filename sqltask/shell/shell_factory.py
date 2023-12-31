import pyperclip
from rich.console import Console
from rich.syntax import Syntax

from sqltask.database.sql_runner import (CommitTransactionExitListener,
                                         RollbackTransactionExitListener,
                                         SQLRunner)
from sqltask.docugen.template_filler import TemplateFiller
from sqltask.shell.prompt import (ActionRegistry, Editor, EditTemplateAction,
                                  ExitAction, InteractiveSQLTemplateRunner,
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


class ShellBuilder2:
    def __init__(self):
        self._project = None
        self._displayer = None
        self.render_listeners = None

    def build(self):
        toreturn = ShellFactory(self._project, self._displayer).make_sqltask_shell()
        return toreturn

    def project(self, project):
        self._project = project
        return self

    def displayer(self, displayer):
        self._displayer = displayer
        return self


class InteractiveSQLTemplateRunnerBuilder:
    def __init__(self, project=None, displayer=None):
        self.project = project
        self.displayer = displayer
        self.template_rendered_listeners = []
        self.exit_listeners = []
        self._commit_rendered_sql = False

    def append_template_rendered_listener(self, listener):
        self.template_rendered_listeners.append(listener)

    def append_exit_listener(self, listener):
        self.exit_listeners.append(listener)

    @staticmethod
    def default(project):
        builder = InteractiveSQLTemplateRunnerBuilder(project)
        sql_runner = SQLRunner(project.db)
        builder.sql_runner = sql_runner
        builder.displayer = PrintSQLToConsoleDisplayer()
        builder.template_rendered_listeners.append(builder.displayer)
        return builder

    def commit_rendered_sql(self):
        self._commit_rendered_sql = True

    def build(self):
        return InteractiveSQLTemplateRunner(self._make_actions_registry())

    def _make_actions_registry(self):
        registry = ActionRegistry()
        registry.register(self.make_process_template_action())
        registry.register(self.make_exit_action())

        return registry

    def make_process_template_action(self):
        library = self.project.library()

        loader = EMTemplatesEnv(library)
        process_template_action = ProcessTemplateAction(
            loader,
            self.make_render_template_action(library, loader),
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

    def make_render_template_action(self, library, loader):
        context_builder = ContextBuilder(self.project)
        context = context_builder.build()
        template_filler = TemplateFiller(initial_context=context)

        template_filler.append_listener(self.sql_runner)
        for listener in self.template_rendered_listeners:
            template_filler.append_listener(listener)
        return RenderTemplateAction(template_filler, loader)

    def make_exit_action(self):
        exit_action = ExitAction()
        for listener in self.exit_listeners:
            exit_action.append_listener(listener)
        if self._commit_rendered_sql:
            exit_action.append_listener(CommitTransactionExitListener(self.sql_runner))
            exit_action.append_listener(
                RollbackTransactionExitListener(self.sql_runner)
            )
        return exit_action

    def make_transaction_decorator(self, sql_runner):
        return RollbackTransactionExitListener(sql_runner)
