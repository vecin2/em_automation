from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
#import click
from fuzzyfinder import fuzzyfinder
from sql_gen.emproject import addb

result =addb.query("SELECT NAME FROM EVA_ENTITY_DEFINITION")
entity_names=[]
for key in result:
    print(entity_names.append(key['NAME']))

print (str(entity_names))
SQLKeywords = ['select', 'from', 'insert', 'update', 'delete', 'drop']

class SQLCompleter(Completer):
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, entity_names)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))

while 1:
    user_input = prompt(u'SQL>',
                        history=FileHistory('history.txt'),
                        completer=SQLCompleter(),
                        )
