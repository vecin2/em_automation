import time

import cx_Oracle
import pymssql
import sql_gen
from sql_gen.database.sqlparser import RelativeIdLoader, SQLParser
from sql_gen.database.sqltable import SQLRow, SQLTable
from sql_gen.exceptions import DatabaseError


class Connector(object):
    """It acts a wrapper of several connector libraries. This allows to use different types of DBs, e.g. sqlserver or oracle."""

    def __init__(
        self,
        server=None,
        user=None,
        password=None,
        database=None,
        port=None,
        dbtype=None,
    ):
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.dbtype = dbtype

    def connect(self):
        try:
            cursor = self.do_connect()
        except Exception as excinfo:
            sql_gen.logger.exception(excinfo)
            raise DatabaseError(
                "Unable to connect to database with params:\n  name="
                + self.database
                + "\n  port="
                + str(self.port)
                + "\n  user="
                + self.user
                + "\nReason was: "
                + str(excinfo)
                + ".\nIf you change EM config properties, for the changes to be picked you need to run 'ccadmin show-config -Dformat=txt'"
            )

        if not cursor:
            raise ValueError(self._get_conn_error_msg(self.dbtype))
        else:
            return cursor

    def do_connect(self):
        if self.dbtype == "sqlServer":
            return pymssql.connect(
                self.server, self.user, self.password, self.database, port=self.port
            )
        elif self.dbtype == "oracle":
            dsn_tns = self.server + ":" + self.port + "/" + self.database

            return cx_Oracle.connect(self.user, self.password, dsn_tns)
        else:
            return None

    def _get_conn_error_msg(self, dbtype):
        help_msg = (
            "Please make sure you configure a valid database type (sqlserver, oracle)"
        )

        if not dbtype:
            error_msg = help_msg
        else:
            error_msg = "'" + dbtype + "' database type is not supported. " + help_msg

        return error_msg


class EMDatabase(object):
    def __init__(self, connector=None):
        self.connector = connector
        self._connection = None
        self.queries_cache = {}

    def rollback(self):
        self._conn().rollback()

    def clearcache(self):
        self.queries_cache = {}
        RelativeIdLoader.clearcache()

    def clear_cache_item(self, key):
        self.queries_cache.pop(key)

    def list(self, query):
        sql_gen.logger.debug("Running list of query")
        table = self.fetch(query)

        if not table:  # if query return no results
            return table
        else:
            return self._first_column(table)

    def _first_column(self, table):
        first_column_name = next(iter(table[0]))
        result = [row[first_column_name] for row in table]

        return result

    def find(self, query):
        result = self.fetch(query)

        if not result or len(result) > 1:
            raise LookupError(
                "Expected to find one record but query '"
                + query
                + "' returned None or more than one. If you expect more that one record"
                + " use fetch instead"
            )

        return result[0]

    def fetch(self, query):
        if query in self.queries_cache:
            sql_gen.logger.debug("Returning from cache")

            return self.queries_cache[query]
        cursor = self._run_query(query)
        result = SQLTable(self._extract_rowlist(cursor))
        self.queries_cache[query] = result

        return result

    def _run_query(self, query):
        start_time = time.time()
        cursor = self.execute(query)
        query_time = str(time.time() - start_time)
        sql_gen.logger.debug("Query run: " + query)
        sql_gen.logger.debug("Query tooked " + query_time)

        return cursor

    def execute(self, query, sqlparser=SQLParser(), commit=False, verbose="q"):
        cursor = self._conn().cursor()

        for statement in self._parse_statements(query):
            try:
                cursor.execute(statement)

                if verbose == "v":
                    print(
                        "\n"
                        + statement
                        + "\nReturned "
                        + str(cursor.rowcount)
                        + " row(s)"
                    )
            except Exception as excinfo:
                print(
                    "The following statement failed:\n" + statement + "\n"
                    "Due to: " + str(excinfo)
                )
                raise

        if commit:
            self.commit()

        return cursor

    def commit(self):
        self._conn().commit()

    def _parse_statements(self, query):
        return SQLParser(RelativeIdLoader(self)).parse_runnable_statements(query)

    def _conn(self):
        if not self._connection:
            self._connection = self.connector.connect()

        return self._connection

    def _extract_rowlist(self, cursor):
        columns = [i[0] for i in cursor.description]
        result = [SQLRow(zip(columns, row)) for row in cursor]

        return result
