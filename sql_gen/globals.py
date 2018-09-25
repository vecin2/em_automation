
def camelcase(st):
    output = ''.join(x for x in st.title() if x.isalnum())
    return output[0].lower() + output[1:]

import pymssql
import sys

def dbquery():
    host = 'windows'
    username = 'pp'
    password = 'pp'
    database = 'pp'
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
    return dict(foo='bar')

