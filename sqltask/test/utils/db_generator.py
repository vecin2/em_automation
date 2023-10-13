from sqltask.test.utils.fake_connection import FakeDBSchema, FakeOracleDatabase


class OracleDatabaseGenerator:
    def __init__(self):
        self.schemas = {}
        self.connection = None

    def add_schema(self, name, tables):
        self.schemas[name] = tables

    def generate(self):
        db = FakeOracleDatabase()

        for schema_name, tables in self.schemas.items():
            db.add_schema(FakeDBSchema(schema_name, tables))

        return db


class QuickOracleDatabaseGenerator:
    def __init__(self):
        self.dbgenerator = OracleDatabaseGenerator()

    def generator(self):
        self.dbgenerator.add_schema("ad", {"CE_CUSTOMER"})

        return self.dbgenerator
