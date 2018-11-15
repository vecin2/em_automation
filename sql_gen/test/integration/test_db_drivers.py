import cx_Oracle
import pymssql
import pytest

sqlserver_host ="windows"
sqlserver_username="sa"
sqlserver_password="admin"
sqlserver_database="ootb_15_1_fp2"
sqlserver_port=1433

oracle_host ="oracle"
oracle_username="SPEN_3PD"
oracle_password="SPEN_3PD"
oracle_database="orcl12c"
oracle_port=1521

def test_pymssql_fetchone_asdict():
    conn = pymssql.connect(sqlserver_host,
                            sqlserver_username,
                            sqlserver_password,
                            sqlserver_database,
                            port=sqlserver_port)
    cursor = conn.cursor(as_dict=True)
    cursor.execute("SELECT * FROM EVA_VERB where NAME='create'")
    assert "create" == cursor.fetchone()['NAME']

def test_oracle_query():
    dsn_tns = cx_Oracle.makedsn("oracle",1521,"orcl12c")
    conn = cx_Oracle.connect(oracle_username,oracle_password,dsn_tns)
    cursor = conn.cursor()
    cursor.execute("SELECT NAME, ID FROM EVA_VERB WHERE NAME='create'")
    assert "create" ==cursor.fetchone()[0]

def rows_to_dict_list(cursor):
    columns = [i[0] for i in cursor.description]
    return [dict(zip(columns, row)) for row in cursor]

def test_convert_oracle_cursor_to_dict_list():
    dsn_tns = cx_Oracle.makedsn("oracle",1521,"orcl12c")
    #conn = cx_Oracle.connect("SPEN_3PD","SPEN_3PD",dsn_tns)
    conn = cx_Oracle.connect("SPEN_3PD","SPEN_3PD",dsn_tns)
    cursor = conn.cursor()
    cursor.execute("SELECT NAME, ID FROM EVA_VERB WHERE NAME='create'")
    result = rows_to_dict_list(cursor)
    assert 118 == len(result)
    assert 'create' == result[0]['NAME']

def test_convert_sqlserver_cursor_to_dict_list():
    host ="windows"
    username="sa"
    password="admin"
    database="ootb_15_1_fp2"
    conn = pymssql.connect(host,
                            username,
                            password,
                            database=database)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EVA_VERB where NAME='create'")
    result = rows_to_dict_list(cursor)
    assert 121 == len(result)
    assert 'create' == result[0]['NAME']


