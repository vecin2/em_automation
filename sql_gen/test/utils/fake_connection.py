class FakeCursor:
    def __init__(self):
        self.executed_sql = ""
        self.description = [[]]
        self.results = []

    def __iter__(self):
        return self.results.__iter__()

    def execute(self, sql):
        self.executed_sql += sql

    @property
    def rowcount(self):
        return len(self.results)


class FakeConnection:
    def __init__(self):
        self._cursor = FakeCursor()
        self.rollbacked = False
        self.committed = False

    def cursor(self):
        return self._cursor

    def set_cursor_execute_results(self, columns, results):
        self._cursor.description = []
        for column in columns:
            self._cursor.description.append([column])

        self._cursor.results = results

    def rollback(self):
        self.rollbacked = True

    def commit(self):
        self.committed = True
