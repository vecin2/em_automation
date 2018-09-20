import signal

# Hanlding Ctrl+C without printing full exception trace
def handler_sigint(signum, frame):
    print( '\n KeyboardInterrupt exception')
    exit()

def do_not_print_stack_trace_on_ctrl_c():
    signal.signal(signal.SIGINT, handler_sigint)

def input_with_validation(text):
    try:
        value = input(text)
        return value
    except EOFError:
        #If Ctrl+D is enter exit the program
        print("\n\nEOF entered. Exiting.")
        exit()
