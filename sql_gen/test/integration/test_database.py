from sql_gen.database import EMDatabase,Connector
import cx_Oracle
import pymssql
import pytest

sqlserver_host ="windows"
sqlserver_username="sa"
sqlserver_password="admin"
sqlserver_database="ootb_15_1_fp2"
sqlserver_port=1433
sqlserver_conn=Connector(sqlserver_host,
                  sqlserver_username,
                  sqlserver_password,
                  sqlserver_database,
                  sqlserver_port,
                  "sqlServer")
sqlserver_db = EMDatabase(sqlserver_conn)

oracle_host ="oracle"
oracle_username="SPEN_3PD"
oracle_password="SPEN_3PD"
oracle_database="orcl12c"
oracle_port=1521
oracle_conn = Connector(oracle_host,
                  oracle_username,
                  oracle_password,
                  oracle_database,
                  oracle_port,
                  "oracle")
oracle_db = EMDatabase(oracle_conn)

testdata=[oracle_db,sqlserver_db]

def test_connect_with_unknown_dbtype_throws_value_error():
    #no need to test with multiple dbs
    dbtype = "oraclesss"
    connection=    Connector(oracle_host,
                          oracle_username,
                          oracle_password,
                          oracle_database,
                          oracle_port,
                          dbtype)
    with pytest.raises(ValueError) as e_info:
        connection.connect()
    assert "'oraclesss' database type is not supported" in str(e_info.value)

@pytest.mark.parametrize("database", testdata)
def test_find_with_duplicate_column_names_uses_last_column(database):
    """it return a dictionary for that row"""
    query ="""SELECT V.ID, PDR.ID
FROM EVA_VERB V, EVA_PROCESS_DESC_REFERENCE PDR
WHERE V.PROCESS_DESC_REF_ID = PDR.ID
AND V.ID = 644"""
    result_dict =database.find(query)
    assert 641 == result_dict["ID"]

