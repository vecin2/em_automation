import pytest
from sql_gen.database.sqltable import SQLTable,SQLRow,Matcher


def test_list_of_dicts():
    dict_list=[]
    search={"ID":1,"NAME":"search"}
    inlinelist={"ID":2,"NAME":"inlinelist"}
    dict_list.append(search)
    dict_list.append(inlinelist)
    assert 1 == dict_list[0]["ID"]
    """"""
@pytest.fixture
def table():
    rows=[SQLRow({"ID":1,"NAME":"search"}),
          SQLRow({"ID":2,"NAME":"inlinelist"})]
    table = SQLTable(rows)
    yield table

def test_table_accesor(table):
    assert 1 == table[0]["ID"]
    assert "search" == table[0]["NAME"]
    assert 2 == table[1]["ID"]
    assert "inlinelist" == table[1]["NAME"]

def test_table_where(table):
    assert 1 == table.where(name="search")[0]["ID"]
    assert "search" == table.where(id="1")[0]["NAME"]
    assert 1 == table.where(name="search",id=1)[0]["ID"]
    assert 0 == len(table.where(name="search",id=2))
    #assert 1 == len(table.where("ID >1"))

def run_match_test(value1 ,value2):
    return Matcher.match(value1,value2)
def test_comparator():
    assert True == run_match_test(1,1)
    assert True == run_match_test(1,"1")
    assert True == run_match_test("1",1)
    assert True == run_match_test("1",1)
