from sql_gen.emproject import current_emproject
import pymssql

class EMDatabase(object):
    def __init__(self,host,username,password, database):
        self.conn = pymssql.connect(host,
                                    username,
                                    password,
                                    database)
    def query(self, query):
        conn = pymssql.connect(host, username, password, database)
        cursor = conn.cursor(as_dict=True)
        cursor.execute(query)
        result = self._extract_rowlist(cursor)
        conn.commit()
        conn.close()
        return result

    def _extract_rowlist(self,cursor):
        result=[]
        for row in cursor:
            result.append(row)
        return result

def addb():
    emconfig = current_emproject.config()
    host = emconfig['database.host']
    username = emconfig['database.admin.user']
    password = emconfig['database.admin.pass']
    database = emconfig['database.logical-schema']

    return EMDatabase(host,
                     username,
                     password,
                     database)

def dbquery_example():
    host = 'windows'
    username = 'sa'
    password = 'admin'
    database = 'ootb_15_1_fp2'
    conn = pymssql.connect(host, username, password, database)
    cursor = conn.cursor(as_dict=True)
    query ='''SELECT * FROM CCADMIN_IDMAP where KEYSET = %s '''
    releaseName= 'Project_R1_0_0'
    keyset ='CC'

    cursor.execute(query,(keyset))
    result=[]
    for row in cursor:
        result.append(row['KEYNAME'])
    conn.commit()
    conn.close()
    return result
