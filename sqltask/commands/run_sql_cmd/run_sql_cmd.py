from sqltask.shell.shell_factory import PrintSQLToConsoleDisplayer
from sqltask.database.sql_runner import (CommitTransactionExitListener,
                                         SQLRunner)
from sqltask.docugen.template_filler import TemplateFiller
from sqltask.shell.prompt import (ActionRegistry, ExitAction,
                                  InteractiveTaskFinder, ProcessTemplateAction,
                                  RenderTemplateAction, ViewTemplateInfoAction)
from sqltask.sqltask_jinja.context import ContextBuilder
from sqltask.sqltask_jinja.sqltask_env import EMTemplatesEnv


class RunSQLCommand:
    def __init__(self, project=None):
        self.project = project

    def run(self):
        finder = InteractiveTaskFinder(self._create_actions_registry())
        finder.run()

    def _create_actions_registry(self):
        registry = ActionRegistry()
        library = self.project.library()
        loader = EMTemplatesEnv(library)
        context_builder = ContextBuilder(self.project)
        context = context_builder.build()
        template_filler = TemplateFiller(initial_context=context)
        sql_runner = SQLRunner(self.project.db)
        template_filler.append_listener(sql_runner)
        template_filler.append_listener(PrintSQLToConsoleDisplayer())

        render_template_action = RenderTemplateAction(template_filler, loader)
        process_template_action = ProcessTemplateAction(loader, render_template_action)
        registry.register(process_template_action)
        process_template_action.register("--info", ViewTemplateInfoAction())
        exit_action = ExitAction()
        exit_action.append_listener(CommitTransactionExitListener(sql_runner))
        registry.register(exit_action)
        return registry
