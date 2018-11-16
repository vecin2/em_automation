import pymssql
import cx_Oracle
from sql_gen.logger import logger
from sql_gen.exceptions import DBConnectionException
import time

class SQLRow(dict):
    def __init(self, dict_row):
        dict.__init__(self,dict_row)

    def __getitem__(self,key):
        if dict.__getitem__(self,key) is None:
            return "NULL"
        return dict.__getitem__(self,key)

class ConnFactory(object):
    """It acts a wrapper of several connection libraries. This allows to use different types of DBs, e.g. sqlserver or oracle."""
    def make_conn(self,
                 server=None,
                 user=None,
                 password=None,
                 database=None,
                 port=None,
                 dbtype=None):
        if dbtype == "sqlserver":
            return pymssql.connect(server,
                                    user,
                                    password,
                                    database,
                                    port=port)
        elif dbtype =="oracle":
            dsn_tns = cx_Oracle.makedsn(server,port,database)
            return cx_Oracle.connect(user,password,dsn_tns)
        else:
            raise ValueError(self._get_conn_error_msg(dbtype))

    def _get_conn_error_msg(self,dbtype):
        help_msg="Please make sure you configure a valid database type (sqlserver, oracle)"
        if not dbtype:
            error_msg =help_msg
        else:
            error_msg="'"+dbtype+"' database type is not supported. "+help_msg
        return error_msg 


class EMDatabase(object):
    ad_singleton = None

    def __init__(self,
                 server=None,
                 user=None,
                 password=None,
                 database=None,
                 port=None,
                 dbtype=None,
                 conn_factory=ConnFactory()):
        self.host = server
        self.username = user
        self.password = password
        self.database = database
        self.port =port
        self.dbtype =dbtype
        self.conn_factory = conn_factory
        self.queries_cache ={}
        self.__conn =None

    def set_conn_factory(self, dbdriver_factory):
        self.conn_factory =dbdriver_factory

    def find(self,query):
        result = self.query(query)
        if not result or len(result)>1:
            raise LookupError("Expected to find one record but query returned None or more than one. If you expect more that one record use fetch instead")
        return result[0]

    def query(self, query):
        #import pdb;pdb.set_trace()
        if query in self.queries_cache:
            logger.debug("Returning from cache")
            return self.queries_cache[query]
        cursor = self._run_query(query)
        result = self._extract_rowlist(cursor)
        self.queries_cache[query]=result
        return result

    def _run_query(self,query):
        conn = self._conn()
        cursor = conn.cursor()
        start_time = time.time()
        cursor.execute(query)
        query_time = str(time.time() - start_time)
        logger.debug("Query "+query+ " took "+ query_time+ " to run")
        return cursor

    def list(self,query):
        logger.debug("Running list of query")
        table = self.query(query)
        if not table:
            return table
        first_column_name = next(iter(table[0]))
        result = [row[first_column_name] for row in table]
        logger.debug("Returning column:"+first_column_name)
        return result

    def _conn(self):
        return self.conn_factory.make_conn(self.host,
                                       self.username,
                                       self.password,
                                       self.database,
                                       self.port,
                                       self.dbtype)

        return self.__conn
    def _extract_rowlist(self,cursor):
        start_time = time.time()
        columns = [i[0] for i in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor]
        convert_time = str(time.time() - start_time)
        logger.debug("Extract  dictionary list from query took "+ convert_time)
        return result
    #def _extract_rowlist(self,cursor):
    #    result=[]
    #    for row in cursor:
    #        result.append(SQLRow(row))
    #    return result

def _addb():
    pass
#this is singleton, otherwise cache will not work
addb = _addb()
