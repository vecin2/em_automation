import os
from pathlib import Path

from sqltask.app_project import AppProject
from sqltask.database.sql_runner import (CommitTransactionExitListener,
                                         SQLRunner)
from sqltask.docugen.template_filler import TemplateFiller
from sqltask.main.project_home import ProjectHome
from sqltask.shell.prompt import (ActionRegistry, ExitAction,
                                  InteractiveSQLTemplateRunner, ProcessTemplateAction,
                                  RenderTemplateAction, ViewTemplateInfoAction)
from sqltask.sqltask_jinja.context import ContextBuilder
from sqltask.sqltask_jinja.sqltask_env import EMTemplatesEnv

project_home = ProjectHome(os.getcwd(), os.environ)
project = AppProject(project_home.path())
cwd_library = Path(os.getcwd()) / ".library"
if cwd_library.exists():
    project.set_library_path(Path(cwd_library.read_text().strip()))
library = project.library()
registry = ActionRegistry()


loader = EMTemplatesEnv(library)
context_builder = ContextBuilder(project)
context = context_builder.build()
template_filler = TemplateFiller(initial_context=context)
sql_runner = SQLRunner(project.db)
template_filler.append_listener(sql_runner)

render_template_action = RenderTemplateAction(template_filler, loader)
process_template_action = ProcessTemplateAction(loader, render_template_action)
registry.register(process_template_action)
process_template_action.register("--info", ViewTemplateInfoAction())
exit_action = ExitAction()
exit_action.append_listener(CommitTransactionExitListener(sql_runner))
registry.register(exit_action)


finder = InteractiveSQLTemplateRunner(registry)
finder.run()
