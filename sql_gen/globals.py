from sql_gen.emproject import current_emproject
import pymssql
import sys

def camelcase(st):
    output = ''.join(x for x in st.title() if x.isalnum())
    return output[0].lower() + output[1:]

def prj_prefix():
    return EMProject.prefix()

def _extract_rowlist(cursor):
    result=[]
    for row in cursor:
        result.append(row)
    return result

def dbquery(query):
    emconfig = emconfig()
    host = emconfig['host']
    username = emconfig['database.admin.user']
    password = emconfig['database.admin.pass']
    database = emconfig['database.logical-schema']
    conn = pymssql.connect(host, username, password, database)

    cursor = conn.cursor(as_dict=True)
    cursor.execute(query)
    result = _extract_rowlist(cursor)
    conn.commit()
    conn.close()
    return result

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
