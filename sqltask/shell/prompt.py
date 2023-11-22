from argparse import ArgumentParser

from prompt_toolkit.completion import Completer, FuzzyWordCompleter
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax

from sqltask.ui.utils import prompt


class ViewTemplateInfoDisplayer:
    def display(self, inline_info):
        console = Console()
        with console.pager(styles=True):
            console.print(*inline_info.displayable_segments())


class TemplateInlineInfo:
    def __init__(self, template):
        self.template = template

    def displayable_segments(self):
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


class ViewTemplateInfoAction:
    """
    Wraps a template displayer into action to it can when the template is selected
    on the prompt
    """

    def __init__(self, library=None):
        self.library = library
        self.displayer = ViewTemplateInfoDisplayer()

    def append_args(self, argparser):
        argparser.add_argument("--view", action="store_true")

    def handles(self, args):
        return args.view

    def run(self, template):
        template = self.library.load_template(template)
        self.displayer.display(TemplateInlineInfo(template))


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
        action = self.actions[self.get_action_name(input)]
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


class InteractiveTaskFinder:
    def __init__(self, registry):
        self.action_registry = registry
        self._completer = InteractiveTaskCompleter(self.action_registry)
        self.max_no_trials = 10

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
            raw_input = prompt("Choose template: ", completer=self._completer)
            if self.parse_and_evaluate(raw_input):
                return True
        raise ValueError("Attempts to select a valid option exceeded.")

    def parse_and_evaluate(self, raw_input):
        input_words = raw_input.split()
        action = self.action_registry.find(input_words[0].strip())
        if not action:
            return False

        action.run(input_words)
        return True
