from argparse import ArgumentParser

from prompt_toolkit.completion import Completer, FuzzyWordCompleter

from sqltask.ui.utils import prompt

# class ActionsCompleter():
#     def make_from(actions):
#         action_names = [action.name for action in actions]
#         return ActionsCompleter(FuzzyWordCompleter(action_names))
#
#     def __init__(self, actions):
#         self.actions = actions
#         self.action_names_completer = FuzzyWordCompleter(actions)
#
#     def _get_actions_completer(self):
#         if not self._actions_completer:
#             action_names = [action.name for action in self.actions]
#             self._actions_completer = ActionsCompleter(FuzzyWordCompleter(action_names))
#         return self._actions_completer
#
#     def get_completions(self, document, complete_event):
#         if self.is_typing_action(document):
#             return self.actions_completer.get_completions(document, complete_event)
#         else:  # is typing action args
#             action = self.get_action(document.get_word_under_cursor())
#             action_args_completer.set_action(self.get_action(action_name))
#             return self.get
#         return []
#
#     def is_typing_action(self, document):
#         words = document.current_line.split(" ")
#         current_word_index = words.index(document.get_word_under_cursor())
#         return current_word_index == 0


class ViewTemplateInfoAction:
    """
    Wraps a template displayer into action to it can when the template is selected
    on the prompt
    """

    def __init__(self, displayer=None):
        self.displayer = displayer

    def append_args(self, argparser):
        argparser.add_argument("--view", action="store_true")

    def handles(self, args):
        return args.view

    def run(self, template):
        self.displayer.display_info(template)


class RenderTemplateAction:
    def run(self, args):
        print("Im running render template")


class ProcessTemplateAction:
    def __init__(self, library, default_action):
        self.library = library
        self.actions = {"default": default_action}
        self.argparser = ArgumentParser()

    @property
    def library_templates(self):
        return self.library.list_all()

    def subaction_names(self):
        return [action for action in self.actions.keys() if action != "default"]

    def register(self, name, action):
        self.actions[name] = action
        action.append_args(self.argparser)

    def register_on(self, registry):
        for template in self.library_templates:
            registry.add_entry(str(template.location()), self)

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
    def append_to(self, completer):
        completer.append_action("exit")

    def register_on(self, registry):
        registry.add_entry("exit", self)

    def run(self, input_words):
        raise EOFError()

    def subaction_names(self):
        # no args for exit
        return []


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
        return self._get_action_args_completer(document).get_completions(
            document, complete_event
        )

    def _get_action_names_completer(self):
        if not self._action_names_completer:
            self._action_names_completer = FuzzyWordCompleter(
                self._action_registry.all_action_names()
            )
        return self._action_names_completer

    def _get_action_args_completer(self, document):
        action = self._action_registry.find(self._get_action_name(document))
        args_completer = FuzzyWordCompleter(action.subaction_names())
        return args_completer


class InteractiveTaskFinder:
    def __init__(self, library):
        self.library = library
        self._registry = None
        self._completer = InteractiveTaskCompleter(self.action_registry)

    @property
    def action_registry(self):
        if not self._registry:
            self._registry = ActionRegistry()
            process_template_action = ProcessTemplateAction(
                self.library, RenderTemplateAction()
            )
            process_template_action.register("--info", ViewTemplateInfoAction())
            self._registry.register(process_template_action)
            self._registry.register(ExitAction())
        return self._registry

    def run(self):
        try:
            while True:
                raw_input = prompt("Choose template: ", completer=self._completer)
                self.evaluate(raw_input)
        except EOFError:
            # Exiting Prompt
            pass

    def evaluate(self, raw_input):
        input_words = raw_input.split()
        action = self.action_registry.find(input_words[0].strip())
        if action:
            action.run(input_words)
