class DisplayTemplateInfoHandler(TemplateHandler):
    def configure(argparser):
        argparser.add_argument("--info", action="store_true")

    def handles(args):
        return args.info

    def handle(args):
        args.template


# create args object if valid otherwise returns None and get_error() returns the error to display
class InputParser:
    def __init__(self):
        self.argparser = ArgumentParser()

    def parse(self, input_str):
        try:
           args = self.argparser.parse(input_str.split(" "))
        except ValueError as excinfo:
            self.error = excinfo
            return

        if 

        for handler in handlers:  # two handlers ExitHandler and ProcessTemplate
            if handler.handles(input_str):
                handler.handle(input_str)


class ExitAction:
    """"""


class TemplateAction:
    def __init__(template):
        self.template = template

    def handles():
        print("hi")

    def handler():
        print("bi")
