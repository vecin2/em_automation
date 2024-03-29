from __future__ import unicode_literals
from prompt_toolkit.completion import Completer, Completion
from fuzzyfinder import fuzzyfinder
import sqltask
import os

logger = sqltask.logger

__all__ = [
    "SuggestionCompleter",
    "PathCompleter",
    "ExecutableCompleter",
]


class SuggestionCompleter(Completer):
    def __init__(self, suggestions):
        self.suggestions = suggestions

    def get_completions(self, document, complete_event):
        sqltask.logger.debug("Running get_completing within SuggestionCompleter")
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, self.suggestions)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))
        sqltask.logger.debug("Finished get_completing within SuggestionCompleter")


# This is o copy of  prompt_toolkit.completion.filsystem
class PathCompleter(Completer):
    """
    Complete for Path variables.
    :param get_paths: Callable which returns a list of directories to look into
                      when the user enters a relative path.
    :param file_filter: Callable which takes a filename and returns whether
                        this file should show up in the completion. ``None``
                        when no filtering has to be done.
    :param min_input_len: Don't do autocompletion when the input string is shorter.
    """

    def __init__(
        self,
        only_directories=False,
        get_paths=None,
        file_filter=None,
        min_input_len=0,
        expanduser=False,
        separator="."
    ):
        assert get_paths is None or callable(get_paths)
        assert file_filter is None or callable(file_filter)
        assert isinstance(min_input_len, int)
        assert isinstance(expanduser, bool)

        self.only_directories = only_directories
        self.get_paths = get_paths or (
            lambda: [os.environ["EM_CORE_HOME"] + "/repository/default", "."]
        )
        self.file_filter = file_filter or (lambda _: True)
        self.min_input_len = min_input_len
        self.expanduser = expanduser

    def get_completions(self, document, complete_event):
        logger.debug("Running get_completing within PathCompleter")
        text = document.text_before_cursor
        text = text.replace(".", "/")

        # Complete only when we have at least the minimal input length,
        # otherwise, we can too many results and autocompletion will become too
        # heavy.
        if len(text) < self.min_input_len:
            return

        try:
            # Do tilde expansion.
            if self.expanduser:
                text = os.path.expanduser(text)

            # Directories where to look.
            dirname = os.path.dirname(text)
            if dirname:
                directories = [
                    os.path.dirname(os.path.join(p, text)) for p in self.get_paths()
                ]
            else:
                directories = self.get_paths()

            # Start of current file.
            prefix = os.path.basename(text)

            # Get all filenames.
            filenames = []
            for directory in directories:
                # Look for matches in this directory.
                if os.path.isdir(directory):
                    for filename in os.listdir(directory):
                        if filename.startswith(prefix):
                            filenames.append((directory, filename))

            # Sort
            filenames = sorted(filenames, key=lambda k: k[1])

            # Yield them.
            for directory, filename in filenames:
                completion = filename[len(prefix) :]
                full_name = os.path.join(directory, filename)

                if os.path.isdir(full_name):
                    # For directories, add a slash to the filename.
                    # (We don't add them to the `completion`. Users can type it
                    # to trigger the autocompletion themselves.)
                    filename += "."
                elif self.only_directories:
                    continue

                if not self.file_filter(full_name):
                    continue

                yield Completion(completion, 0, display=filename)
        except OSError:
            pass
        logger.debug("Finished get_completing within PathCompleter")


class ExecutableCompleter(PathCompleter):
    """
    Complete only executable files in the current path.
    """

    def __init__(self):
        PathCompleter.__init__(
            self,
            only_directories=False,
            min_input_len=1,
            get_paths=lambda: os.environ.get("PATH", "").split(os.pathsep),
            file_filter=lambda name: os.access(name, os.X_OK),
            expanduser=True,
        ),


class SQLCompleter(Completer):
    def __init__(self, suggestions):
        suggestions = ["select", "from", "insert", "update", "delete", "drop"]
        self.suggestions = suggestions

    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, self.suggestions)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))
