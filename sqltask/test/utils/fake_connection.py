class FakeOracleClient:
    def __init__(self, fakedb):
        self.fakedb = fakedb

    def connect(self, user, password, dsn_tns):
        return self.fakedb.connect(user, password, dsn_tns)


class FakeOracleDatabase:
    def __init__(self):
        self.schemas = {}

    def connect(self, user, password, dsn_tns):
        return self.schemas[user].connection()

    def add_schema(self, schema):
        self.schemas[schema.name] = schema

    def executed_sql(self, schema_name):
        return self.schemas[schema_name].executed_sql()


class FakeDBSchema:
    def __init__(self, name, tables):
        self.name = name
        self.tables = tables
        self._executed_sql = ""
        self._connection = None

    def cursor(self):
        return FakeCursor(self)

    def connection(self):
        if not self._connection:
            self._connection = FakeConnection(self.cursor())
        return self._connection

    def executed_sql(self):
        return self._executed_sql

    # def set_cursor_execute_results(self, headers, results):
    #     self._cursor.description = []
    #     for header in headers:
    #         self._cursor.description.append([header])
    #
    #     self._cursor.results = results

    def execute(self, sql):
        self._executed_sql += sql
        table_name = self.get_table_name(sql)
        if table_name not in self.tables:
            raise Exception(f"Table or view does not exist on schema {self.name}")

    def get_table_name(self, sql):
        words = sql.upper().split()
        table_name_idx = self.get_index_of(words, {"FROM", "INTO"}) + 1
        if table_name_idx < len(words):
            return words[table_name_idx]
        return None

    def get_index_of(self, words, subwords):
        for index, word in enumerate(words):
            if word in subwords:
                return index
        joined_words = " ".join(words)
        raise ValueError(f"'{subwords}' is not on in '{joined_words}'")
        return None


class FakeConnection:
    def __init__(self, cursor):
        self._cursor = cursor
        self.rollbacked = False
        self.committed = False

    def cursor(self):
        return self._cursor

    def rollback(self):
        self.rollbacked = True

    def commit(self):
        self.committed = True


class FakeCursor:
    def __init__(self, schema):
        self.schema = schema
        self.description = []
        self.results = [[]]

    def __iter__(self):
        return self.results.__iter__()

    def execute(self, sql):
        self.schema.execute(sql)

    @property
    def rowcount(self):
        return len(self.results)
