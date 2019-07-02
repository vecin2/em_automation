import pytest
from sql_gen.database.sqltable import SQLTable,SQLRow,Matcher,ExpressionFilter


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
    assert 1 == len(table.where("ID >1"))

def test_table_where_string_with_spaces(table):
    displayName="Contact search"
    table.append(SQLRow({"ID":3,"NAME":displayName}))
    assert 3 == table.where("NAME=="+displayName)[0]["ID"]

def test_table_column(table):
    assert [1,2] == table.column("ID")

def test_table_column_invalid_name_raised_exc_if_table_populated(table):
    with pytest.raises (KeyError) as excinfo:
        table.column("IDs")
def test_table_column_invalid_name_returns_empty_if_table_empty(table):
    assert [] == SQLTable().column("IDs")

def run_reg_expression(var1, expected_operator, var2, expression):
    expr_filter = ExpressionFilter(expression)
    assert expected_operator == expr_filter.operator
    assert var1 == expr_filter.key
    assert var2 == expr_filter.value

def fail_reg_expression(message,expression):
    with pytest.raises(ValueError) as excinfo:
        expr_filter = ExpressionFilter(expression)
    assert message in str(excinfo)


def test_expr_filter_constructor():
    fail_reg_expression("Invalid operator '<>'","a <> b")
    run_reg_expression("a","<","b","a<b")
    run_reg_expression("a",">","b","a>b")
    run_reg_expression("a","==","b","a==b")
    run_reg_expression("a","!=","b","a!=b")
    run_reg_expression("a","<=","b","a<=b")
    run_reg_expression("a",">=","b","a>=b")
    run_reg_expression("a","<","b","a < b")
    run_reg_expression("a b","==","a b","a b == a b")

def run_exp_filter_test(expected, expr, table):
    table1 = table.clone()
    expr_filter = ExpressionFilter(expr)
    assert expected == expr_filter.apply(table1).rows

def test_expr_filter(table):
    run_exp_filter_test([{"ID":1,"NAME":"search"}],"ID<2",table)
    run_exp_filter_test([{"ID":2,"NAME":"inlinelist"}],"ID>1",table)
    run_exp_filter_test([{"ID":2,"NAME":"inlinelist"}],"ID>=2",table)
    run_exp_filter_test([{"ID":1,"NAME":"search"},
                         {"ID":2,"NAME":"inlinelist"}],"ID<=2",table)
    run_exp_filter_test([{"ID":1,"NAME":"search"} ],"ID!=2",table)

def run_match_test(value1 ,value2):
    return Matcher.match(value1,value2)

def test_comparator():
    assert True == run_match_test(1,1)
    assert True == run_match_test(1,"1")
    assert True == run_match_test("1",1)
