from prompt_toolkit import prompt
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.key_binding import KeyBindings

bindings = KeyBindings()


@bindings.add("c-r")
def _(event):
    "Say 'hello' when `c-r` is pressed."

    def print_hello():
        print("hello world")

    run_in_terminal(print_hello)


@bindings.add("c-x")
def _(event):
    "Exit when `c-x` is pressed."
    event.app.exit()


text = prompt("> ", key_bindings=bindings)
print("You said: %s" % text)
