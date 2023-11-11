from prompt_toolkit import prompt
from prompt_toolkit.completion import (Completer, Completion, FuzzyCompleter,
                                       FuzzyWordCompleter, WordCompleter)
from prompt_toolkit.document import Document
from prompt_toolkit.validation import ValidationError, Validator


class MyCustomCompleter(Completer):
    def __init__(self):
        self.counter = 0

    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        word_before_cursor = document.get_word_under_cursor(WORD=True)
        print(f"{str(self.counter)}. {word_before_cursor}")
        self.counter += 1
        yield Completion("completion", start_position=0)


# text = prompt("> ", completer=MyCustomCompleter())


class CompositeCompleter(Completer):
    def __init__(self, completers):
        self.completers = completers

    def get_completions(self, document, complete_event):
        words = document.current_line.split(" ")
        current_word_index = words.index(document.get_word_under_cursor())
        if current_word_index < len(self.completers):
            return self.completers[current_word_index].get_completions(
                document, complete_event
            )
        return []


words = ["html", "sql other"]
words2 = ["java", "python"]
words_dict = {
    "html": "this is jesus",
    "sql other": "this is anthon",
}
display_dict = {"html": "html", "sql other": "sql other"}
# html_completer = FuzzyWordCompleter(["<html>", "<body>", "<head>", "<title>"])
html_completer = CompositeCompleter(
    [
        FuzzyCompleter(
            WordCompleter(words, meta_dict=words_dict, display_dict=display_dict)
        ),
        FuzzyWordCompleter(words2),
    ]
)
# html_completer = WordCompleter(['<html>', '<body>', '<head>', '<title>'])
text = prompt("Enter HTML: ", completer=html_completer)
print("You said: %s" % text)


# if cursor_at_first_word():
#     suggest_templates()
# elif cursor_at_second_word() and first_word_matches_a_valid_option():
#     suggest_parameters()

d = Document(text="this is mark.sql = test", cursor_position=15)
print(f"word_under_cursor: {d.get_word_under_cursor(WORD=True)}")
print(f"word_before_cursor: {d.get_word_before_cursor()}")
print(f"current_line: {d.current_line}")
print(f"current_line_length:{len(d.current_line)}")
print(f"current_char: {d.current_char}")
print(f"current_position: {d.cursor_position}")
previous_word_beginning_rel = d.find_previous_word_beginning(2, WORD=False)
print(f"find_previous_word_beginning: {previous_word_beginning_rel}")
print(f"find_start_of_previous_word: {d.find_start_of_previous_word(3)}")
previous_word_beginning = d.current_line[
    d.cursor_position + previous_word_beginning_rel
]
print(f"char at previous word_begining {previous_word_beginning}")

# find_previous_word_beginning


class NumberValidator(Validator):
    def validate(self, document):
        text = document.text

        if text and not text.isdigit():
            i = 0

            # Get index of first non numeric character.
            # We want to move the cursor here.
            for i, c in enumerate(text):
                if not c.isdigit():
                    break

            raise ValidationError(
                message="This input contains non-numeric characters", cursor_position=i
            )


number = int(
    prompt("Give a number: ", validator=NumberValidator(), validate_while_typing=False)
)
print("You said: %i" % number)
