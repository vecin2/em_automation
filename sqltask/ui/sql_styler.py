class SQLStyler:
    def __init__(self, initial_content=None):
        self.string_builder = []
        if initial_content:
            self.append(initial_content)

    def append_sql(self, content):
        if not self.is_empty():
            self.append("\n\n\n")
        self.append(content)

    def is_empty(self):
        return self.text() == ""

    def append(self, sql):
        self.string_builder.append(sql)
        return self

    def text(self):
        return "".join(self.string_builder)
