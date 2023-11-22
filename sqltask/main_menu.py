class MenuOption(object):
    def __init__(self, name, code=""):
        self.code = code
        self.name = name

    @staticmethod
    def saveAndExit():
        return MenuOption("Save && Exit", "x")

    @staticmethod
    def to_options(names):
        template_option_list = []
        for counter, name in enumerate(names):
            template_option = MenuOption(name)
            template_option_list.append(template_option)
        return template_option_list

    def matches(self, input_entered):
        if (
            self.code == input_entered
            or self.name == input_entered
            or input_entered == str(self)
        ):
            return True
        return False

    def __repr__(self):
        if not self.code:
            return self.name

        return f"{self.code}. {self.name}"

    def __eq__(self, other):
        return self.code == other.code and self.name == other.name
