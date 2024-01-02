import os
from argparse import ArgumentParser
from pathlib import Path
from subprocess import check_output

from prompt_toolkit.completion import Completer, FuzzyWordCompleter
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax

from sqltask.ui.utils import prompt


class TemplateInlineInfoView:
    def __init__(self, template):
        self.template = template

    def display(self):
        console = Console()
        console.print(*self._displayable_segments())

    def _displayable_segments(self):
        segments = []
        self._append_metadata_segments(segments)
        self._append_body_segments(segments)
        return segments

    def _append_metadata_segments(self, segments):
        segments.append(Markdown(self.metadata()))

    def metadata(self):
        sb = []
        template_info = self.template.info()
        self._append_lines_with_header(
            "Short Description", sb, template_info.oneline_description()
        )
        self._append_lines_with_header(
            "Description", sb, template_info.long_description()
        )
        self._append_lines_with_header(
            "Related Tasks", sb, template_info.related_tasks()
        )
        self._append_lines_with_header(
            "Related Views", sb, template_info.related_views()
        )
        return "".join(sb)

    def _append_body_segments(self, segments):
        if self.template.has_test():
            segments.append(Markdown("## Test"))
            segments.append(self.sql_syntax(self.template.test_content()))
        else:
            segments.append(Markdown("## Template"))
            segments.append(self.sql_syntax(self.template.content()))

    def sql_syntax(self, sql_text):
        return Syntax(
            sql_text,
            "sql",
            theme="monokai",
            line_numbers=False,
            word_wrap=True,
        )

    def _append_lines_with_header(self, header, sb, text):
        if len(text) > 0:
            self._append_line(sb, f"## {header}")
            self._append_line(sb, text)

    def _append_line(self, sb, line):
        sb.append(line + "\n")

    def _append_text(self, sb, text):
        sb.append(text)


class Git:
    def __init__(self, rootpath):
        self.rootpath = rootpath

    def remote_origin_url(self):
        output = self._run(
            "-C", str(self.rootpath), "config", "--get", "remote.origin.url"
        )
        return output.splitlines()[0]

    def show_current_branch(self):
        output = self._run("-C", str(self.rootpath), "branch", "--show-current")
        return output.splitlines()[0]

    def _run(self, *args):
        return check_output(["git"] + list(args)).decode("utf-8")
        # return subprocess.check_call(["git"] + list(args))


class Browser:
    def __init__(self, browse_cmd):
        self.browse_cmd = browse_cmd

    def open(self, url):
        print("Browsing " + url)
        os.system(self.browse_cmd + " " + url)


class ViewTemplateDocsAction:
    """
    Wraps a template displayer into action to it can when the template is selected
    on the prompt
    """

    def __init__(self, library=None, browse_cmd=None):
        self.library = library
        self.browse_cmd = browse_cmd

    def append_args(self, argparser):
        argparser.add_argument("--docs", action="store_true")

    def handles(self, args):
        return args.docs

    def run(self, template):
        git = self.make_git()
        github_url = self.get_library_repo_url(git)

        docs_url = (
            github_url
            + "/tree/"
            + git.show_current_branch()
            + "/docs/LibraryByFolder.md"
            + self._md_anchor(template)
        )
        Browser(self.browse_cmd).open(docs_url)

    def make_git(self):
        # to allow mocks override this method
        return Git(self.library.rootpath)

    def get_library_repo_url(self, git):
        remote_library_url = git.remote_origin_url()
        if remote_library_url.startswith("http"):
            github_url = remote_library_url
        else:
            # remote_lib_url like git@github.com-verint:verint-CME/sqltask-library.git
            ssh_at_split = remote_library_url.split("@")
            if len(ssh_at_split) > 1:
                repo_split = ssh_at_split[1].split(":")
                if len(repo_split) > 1:
                    repo_path = repo_split[1]
                    github_url = "https://github.com/" + repo_path.split(".git")[0]
        return github_url

    def _md_anchor(self, template):
        template_name = str(Path(template).stem)
        return "#" + template_name.lower().replace("_", "-")


class SystemCmdRunner:
    """
    Abstraction that allows testing edit,info and docs command by intercepting the command that is passed to it

    """

    def execute(self, command_to_run):
        os.system(command_to_run)


class Editor:
    """It takes two string commands with a place holder for the file paths that wil be editing:
    - edit_str_cmd: is the actual command that runs, e.g. vim {}
    - path_converter_cmd: it allows to put a wrapper around each path.
                        Useful to convert linux path into windows, if you are using WSL for example
    """

    def __init__(
        self, edit_str_cmd, path_converter_cmd="{}", cmd_runner=SystemCmdRunner()
    ):
        self.edit_str_cmd = edit_str_cmd
        if not path_converter_cmd:
            # make sure it has one place holder even if it is passed as None
            path_converter_cmd = "{}"
        self.path_converter_cmd = path_converter_cmd
        self.cmd_runner = cmd_runner

    def edit(self, template):
        paths_to_open = str(template.abspath())
        if template.has_test():
            paths_to_open += " " + str(template.abstestpath())

        converted_paths = []
        for path_to_open in paths_to_open.split():
            converted_paths.append(self.path_converter_cmd.format(path_to_open))

        command_to_run = self.edit_str_cmd.format(" ".join(converted_paths))
        self.cmd_runner.execute(command_to_run)


class EditTemplateAction:
    """
    Wraps a template displayer into action to it can when the template is selected
    on the prompt
    """

    def __init__(self, library, editor):
        self.library = library
        self.editor = editor

    def append_args(self, argparser):
        argparser.add_argument("--edit", action="store_true")

    def handles(self, args):
        return args.docs

    def run(self, template):
        template = self.library.load_template(template)
        self.editor.edit(template)


class ViewTemplateInfoAction:
    """
    Wraps a template displayer into action to it can when the template is selected
    on the prompt
    """

    def __init__(self, library=None):
        self.library = library

    def append_args(self, argparser):
        argparser.add_argument("--view", action="store_true")

    def handles(self, args):
        return args.view

    def run(self, template):
        template = self.library.load_template(template)
        TemplateInlineInfoView(template).display()


class RenderTemplateAction:
    def __init__(self, renderer, loader):
        self.renderer = renderer
        self.loader = loader

    def run(self, template_location):
        template = self.loader.get_template(template_location)
        self.renderer.fill_and_render(template)


class ProcessTemplateAction:
    def __init__(self, template_loader, default_action):
        self.template_loader = template_loader
        self.actions = {"default": default_action}
        self.argparser = ArgumentParser()

    @property
    def library_templates(self):
        return self.template_loader.list_visible_templates()

    def subaction_names(self):
        return [action for action in self.actions.keys() if action != "default"]

    def register(self, name, action):
        self.actions[name] = action
        action.append_args(self.argparser)

    def register_on(self, registry):
        for template in self.library_templates:
            registry.add_entry(str(template), self)

    def run(self, input):
        action = self.actions.get(self.get_action_name(input), None)
        if not action:
            # keep prompting
            return
        template_location = input[0]
        action.run(template_location)

    def get_action_name(self, input):
        if len(input) == 1:  # no args
            return "default"  # default to render
        else:
            return input[1]


class ExitAction:
    def __init__(self):
        self.listeners = []

    def append_to(self, completer):
        completer.append_action("exit")

    def register_on(self, registry):
        registry.add_entry("exit", self)

    def run(self, input_words):
        for listener in self.listeners:
            listener.on_finish()
        raise EOFError()

    def subaction_names(self):
        # no args for exit
        return []

    def append_listener(self, listener):
        self.listeners.append(listener)


class ActionRegistry:
    """
    A registry maps an action name with the corresponding action instance
    and it provides completion for the actions
    """

    def __init__(self):
        self.map = {}

    def register(self, action):
        action.register_on(self)

    def add_entry(self, key, action):
        self.map[key] = action

    def find(self, key):
        if key in self.map:
            return self.map[key]

    def all_action_names(self):
        return self.map.keys()


class InteractiveTaskCompleter(Completer):
    """
    It provides completion when searching for task and combines it the completion
    for the specific action
    """

    def __init__(self, action_registry):
        super().__init__()
        self._action_registry = action_registry
        self._action_names_completer = None

    def get_completions(self, document, complete_event):
        if self._cursor_is_on_action(document):
            return self._get_completions_for_action_name(document, complete_event)
        else:  # is typing action args
            return self._get_completions_for_action_args(document, complete_event)
        return []

    def _cursor_is_on_action(self, document):
        words = document.current_line.split(" ")
        current_word_index = words.index(document.get_word_under_cursor(WORD=True))
        return current_word_index == 0

    def _get_action_name(self, document):
        return document.current_line.split()[0]

    def _get_completions_for_action_name(self, document, complete_event):
        return self._get_action_names_completer().get_completions(
            document, complete_event
        )

    def _get_completions_for_action_args(self, document, complete_event):
        action_name = self._get_action_name(document)
        action = self._action_registry.find(action_name)
        if not action:
            return []
        return self._get_action_args_completer(action).get_completions(
            document, complete_event
        )

    def _get_action_names_completer(self):
        if not self._action_names_completer:
            self._action_names_completer = FuzzyWordCompleter(
                self._action_registry.all_action_names()
            )
        return self._action_names_completer

    def _get_action_args_completer(self, action):
        args_completer = FuzzyWordCompleter(action.subaction_names())
        return args_completer


class InteractiveSQLTemplateRunner:
    def __init__(self, registry):
        self.action_registry = registry
        self._completer = InteractiveTaskCompleter(self.action_registry)
        self.max_no_trials = 10
        self.default_prompt_value = ""
        self.default_selection = ""

    def run(self):
        try:
            while True:
                self.prompt_until_valid()
        except EOFError:
            # Exiting Prompt
            pass

    def prompt_until_valid(self):
        trial = 0
        while trial <= self.max_no_trials:
            trial += 1
            raw_input = prompt(
                "Choose template: ",
                completer=self._completer,
                default=self.default_selection,
            )
            if self.parse_and_evaluate(raw_input):
                return True
        raise ValueError("Attempts to select a valid option exceeded.")

    def parse_and_evaluate(self, raw_input):
        input_words = raw_input.split()
        if len(input_words) == 0:
            return False
        action = self.action_registry.find(input_words[0].strip())
        if not action:
            return False

        self._compute_default_selection(input_words)
        action.run(input_words)
        return True

    def _compute_default_selection(self, input_words):
        self.default_selection = ""
        if len(input_words) > 1:
            self.default_selection = input_words[0]
