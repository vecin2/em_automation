from sql_gen.database import EMDatabase
import cx_Oracle
import pymssql
import pytest
from sql_gen.test.utils.db_utils import FakeDBConnectionFactory

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


@pytest.mark.skip
def test_instantiate():
    emdb = EMDatabase("admin","admin123","db_host","sqlserver",username="admin",password="admin123")

@pytest.mark.skip
def  test_fetch_returns_dict_list():
    conn_factory = FakeDBConnectionFactory()
    emdb = EMDatabase("admin","admin123","db_host","sqlserver",username="admin",password="admin123")
    emdb.set_conn_factory(conn_factory)
    query = "SELECT * FROM EVA_VERB"

    result = emdb.query(query)

    assert "admin" == conn_factory.args[0][0]
    assert "admin123" == conn_factory.args[0][1]
    assert "db_host" == conn_factory.args[0][2]
    assert "admin" == conn_factory.args[1]["username"]
    assert "admin123" == conn_factory.args[1]["password"]

