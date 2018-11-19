import signal

def input_with_validation(text):
    try:
        value = input(text)
        return value
    except EOFError:
        #If Ctrl+D is enter exit the program
        print("\n\nEOF entered. Exiting.")
        exit()

class InputRequester(object):
    def __init__(self):
        self.task_already_exists=False

    def request_value(self, text, *args):
        value = input_with_validation(text) 
        if args is not None:
            while value not in args:
                value = input_with_validation(text) 
        return value

