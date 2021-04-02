from sql_gen.sqltask_jinja.filters import PromptFilter
from sql_gen.docugen.completer import SuggestionCompleter


def suggest(value, suggestions):
    return value


def get_template_filter():
    return suggest


class SuggestFilter(PromptFilter):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter

    def apply(self, prompt, context):
        args = self._render_args(context)
        suggestions = self._extract_list_from_arg(args[0])
        prompt.completer = SuggestionCompleter(suggestions)
        return prompt.display_text

    def _extract_list_from_arg(self, suggestions):
        result = []
        for suggestion in suggestions:
            result.append(suggestion)
        return result
