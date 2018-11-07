from sql_gen.emproject import current_emproject
import pymssql
from sql_gen.logger import logger

class SQLRow(dict):
    def __init(self, dict_row):
        dict.__init__(self,dict_row)

    def __getitem__(self,key):
        if dict.__getitem__(self,key) is None:
            return "NULL"
        return dict.__getitem__(self,key)

class Query(object):
    query = None
    def __init__(self):
        self._cache = {}
    #def __call__(self, query):
    #    if query not in self._cache: 
    #        self._cache[a] = self.do_query(query)
    #    return self._cache[query]
    def query(self, query):

        return # a real answer
    @staticmethod
    def get_instance():
        return Query()
        if not Query.query:
            Query.query = Query()
        return Query.query

class EMDatabase(object):
    ad_singleton = None
    
    def __init__(self,host,username,password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.__conn =None
        self.queries_cache ={}

    def query(self, query):
        if query in self.queries_cache:
            logger.debug("Returning from cache")
            return self.queries_cache[query]

        logger.debug("Running query: "+ query)
        conn = self._conn()
        cursor = conn.cursor(as_dict=True)
        logger.debug("About to executed query")
        cursor.execute(query)
        logger.debug("Query excecuted")
        result = self._extract_rowlist(cursor)
        logger.debug("Row list extracted")
        conn.commit()
        #conn.close()
        logger.debug("Finishing running query")
        self.queries_cache[query]=result
        return result

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
        #we cache connection as it takes 3 seconds to run in windows
        if not self.__conn:
            logger.debug("Opening connection with params: ["+self.host +", "+self.username+", "+self.database+"]")
            self.__conn = pymssql.connect(self.host,
                                    self.username,
                                    self.password,
                                    self.database)
            logger.debug("Open connection Succeed")
        return self.__conn

    def _extract_rowlist(self,cursor):
        result=[]
        for row in cursor:
            result.append(SQLRow(row))
        return result

def _addb():
    emconfig = current_emproject.config()
    host = emconfig['database.host']
    username = emconfig['database.admin.user']
    password = emconfig['database.admin.pass']
    database = emconfig['database.logical-schema']
    return EMDatabase(host,
                      username,
                      password,
                      database)
#this is singleton, otherwise cache will not work
addb = _addb()
