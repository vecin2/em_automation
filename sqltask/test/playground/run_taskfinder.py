import os
from pathlib import Path

from sqltask.app_project import AppProject
from sqltask.finder.prompt import InteractiveTaskFinder
from sqltask.main.project_home import ProjectHome

project_home = ProjectHome(os.getcwd(), os.environ)
project = AppProject(project_home.path())
cwd_library = Path(os.getcwd()) / ".library"
if cwd_library.exists():
    project.set_library_path(Path(cwd_library.read_text().strip()))
finder = InteractiveTaskFinder(project.library())

finder.run()
