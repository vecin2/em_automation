from sql_gen.database import EMDatabase
import cx_Oracle
import pymssql
import pytest

sqlserver_host ="windows"
sqlserver_username="sa"
sqlserver_password="admin"
sqlserver_database="ootb_15_1_fp2"
sqlserver_port=1433

sqlserver_db = EMDatabase(sqlserver_host,
                  sqlserver_username,
                  sqlserver_password,
                  sqlserver_database,
                  sqlserver_port,
                  "sqlserver")

oracle_host ="oracle"
oracle_username="SPEN_3PD"
oracle_password="SPEN_3PD"
oracle_database="orcl12c"
oracle_port=1521
oracle_db = EMDatabase(oracle_host,
                  oracle_username,
                  oracle_password,
                  oracle_database,
                  oracle_port,
                  "oracle")

testdata=[oracle_db,sqlserver_db]

def test_connect_with_unknown_dbtype_throws_value_error():
    #no need to test with multiple dbs
    dbtype = "oraclesss"
    emdb = EMDatabase(oracle_host,
                      oracle_username,
                      oracle_password,
                      oracle_database,
                      oracle_port,
                      dbtype)
    with pytest.raises(ValueError) as e_info:
        emdb._conn()
    assert "'oraclesss' database type is not supported" in str(e_info.value)

def test_connect_without_dbtype_throws_value_erro():
    #no need to test with multiple dbs
    dbtype = None
    emdb = EMDatabase(oracle_host,
                      oracle_username,
                      oracle_password,
                      oracle_database,
                      oracle_port,
                      dbtype)
    with pytest.raises(ValueError) as e_info:
        emdb._conn()
    assert "Please make sure you configure a valid database type (sqlserver, oracle)" in str(e_info.value)

@pytest.mark.parametrize("database", testdata)
def test_get_connection(database):
    database._conn()

@pytest.mark.parametrize("database", testdata)
def test_find_returns_dictionary_row(database):
    """it return a dictionary for that row"""
    result_dict =database.find("SELECT * FROM EVA_VERB where ID =644")
    assert 644 == result_dict["ID"]

@pytest.mark.parametrize("database", testdata)
def test_find_with_duplicate_column_names_uses_last_column(database):
    """it return a dictionary for that row"""
    query ="""SELECT V.ID, PDR.ID
FROM EVA_VERB V, EVA_PROCESS_DESC_REFERENCE PDR
WHERE V.PROCESS_DESC_REF_ID = PDR.ID
AND V.ID = 644"""
    result_dict =database.find(query)
    assert 641 == result_dict["ID"]

@pytest.mark.parametrize("database", testdata)
def test_find_with_explictily_select_columns(database):
    """it return a dictionary for that row"""
    query ="""SELECT V.ID as V_ID, PDR.ID as PDR_ID
FROM EVA_VERB V, EVA_PROCESS_DESC_REFERENCE PDR
WHERE V.PROCESS_DESC_REF_ID = PDR.ID
AND V.ID = 644"""
    result_dict =database.find(query)
    assert 644 == result_dict["V_ID"]
    assert 641 == result_dict["PDR_ID"]

def test_find_throws_exception_if_nothing_found():
    #no need to test with multiple dbs
    query ="SELECT * FROM EVA_VERB where ID =-1"
    with pytest.raises(LookupError) as e_info:
        oracle_db.find(query)
    assert "Expected to find one record but query returned None or more than one. If you expect more that one record use fetch instead" == str(e_info.value)

def test_find_throws_exception_if_more_than_one_found():
    #no need to test with multiple dbs
    query ="SELECT * FROM EVA_VERB"
    with pytest.raises(LookupError) as e_info:
        oracle_db.find(query)
    assert "Expected to find one record but query returned None or more than one. If you expect more that one record use fetch instead" == str(e_info.value)

def test_list_will_return_a_list_of_items_in_the_column():
    query ="SELECT * FROM CCADMIN_IDMAP"
    result = oracle_db.list(query)
    assert "PDR" == result[0]

