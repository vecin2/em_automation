from pathlib import Path

from sqltask.commands.create_sql_cmd.task_prefix_generator import \
    TaskPrefixGenerator
from sqltask.ui.utils import prompt, prompt_suggestions


class PathSelectorDisplayer(object):
    def ask_for_sqlmodulename(self, options):
        text = "\nPlease enter the sql module name: "
        return prompt_suggestions(text, options)

    def ask_for_sqltaskname(self, default=None, existing_task_names=None):
        if existing_task_names:
            print(
                "\nExisting tasks on that folder are:\n"
                + ", ".join(existing_task_names)
            )
        else:
            print(
                "\nNo tasks exist in this folder yet. Please follow project naming convention when entering the name, e.g. 01_ExtendCustomer"
            )
        text = "\nPlease enter the task name: "
        return prompt(text, default=default)


class SQLPathSelector(object):
    def __init__(self, modules_root, release_name):
        self.displayer = PathSelectorDisplayer()
        self.modules_root = modules_root
        self.release_name = release_name

    def compute_path(self):
        options = self._get_modules()
        module_name = self.displayer.ask_for_sqlmodulename(options)
        task_folder = self.get_task_folder(module_name)
        sqltask_name = self.displayer.ask_for_sqltaskname(
            default=self._get_current_prefix_number(task_folder),
            existing_task_names=self._list_existing_task_names(task_folder),
        )
        return task_folder / sqltask_name

    def _get_modules(self):
        if not self.modules_root.exists():
            return []
        return list(self.modules_root.iterdir())

    def _get_current_prefix_number(self, folder):
        existing_task_names = self._list_existing_task_names(folder)
        if existing_task_names:
            last_folder = existing_task_names[-1]
            return TaskPrefixGenerator().next(last_folder)
        return ""

    def _list_existing_task_names(self, folder):
        path = Path(folder)
        result = []
        if path.exists():
            existing_task_folders = sorted(path.iterdir())
            for folder in existing_task_folders:
                result.append(folder.name)
        return result


    def get_task_folder(self, module_name):
        return (
            self.modules_root
            / module_name
            / "sqlScripts/oracle/updates"
            / self.release_name
        )

