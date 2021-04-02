import pytest
from sql_gen.database.sqlparser import RelativeId, RelativeIdReplacer, SQLParser


class FakeRelativeIdLoader(object):
    def __init__(self, storage_table=None):
        self.storage_table = storage_table

    def load(self, keyset, keyname):
        return self.storage_table[keyset][keyname]


def assert_relative_ids(expected_list, sqltext):
    assert expected_list == RelativeIdReplacer().find_all(sqltext)


def test_matching_relative_ids():
    assert_relative_ids([], "@CC.Home)")
    assert_relative_ids(["@CC.Home"], "(@CC.Home)")
    assert_relative_ids(["@CC.Home"], ",@CC.Home)")
    assert_relative_ids(["@CC.Home"], " @CC.Home)")
    assert_relative_ids(["@CC.Home"], "'frank.smith@gmail.com',@CC.Home)")
    assert_relative_ids(["@CC.Home"], " @CC.Home,@CC.Home")


def assert_replace_ids(replacer, expected, sqltext):
    assert expected == replacer.replace(sqltext)


def test_replace_ids():
    table = {
        "CC": {"Home": 123, "Admin": 234},
        "ED": {"Agent": 345, "ContactHistory": 567},
    }
    loader = FakeRelativeIdLoader(storage_table=table)
    replacer = RelativeIdReplacer(loader)
    assert_replace_ids(replacer, "(123)", "(@CC.Home)")
    assert_replace_ids(replacer, "(123,123)", "(@CC.Home,@CC.Home)")
    assert_replace_ids(
        replacer,
        "(123,234,345,567)",
        "(@CC.Home,@CC.Admin,@ED.Agent,@ED.ContactHistory)",
    )


def test_remove_comments_and_strip_str():
    sqltext = """ INSERT INTO VERB(ID,NAME)
    VALUES(12, --id
           "search" --name
           ) """
    expected = """INSERT INTO VERB(ID,NAME)
    VALUES(12, "search"  )"""
    assert expected == SQLParser().strip_comments(sqltext)


def test_splits_multiple_runnable_stmts():
    sqltext = """SELECT * FROM VERB;
    SELECT * FROM ENTITY;"""
    stmt1 = "SELECT * FROM VERB"
    stmt2 = "SELECT * FROM ENTITY"
    assert [stmt1, stmt2] == SQLParser().split(sqltext)
    assert [stmt1, stmt2, "--some comment"] == SQLParser().split(
        sqltext + "\n--some comment"
    )


def test_parse_full_sql():
    sqltext = """
--insert entity def
INSERT INTO ENTITY_DEF (ID, ENV_ID, NAME)
VALUES (
	@ED.customerID, --id
       	@ENV.Dflt, --env_id
       	'customer'--name
      );
--insert a verb
INSERT INTO VERB (ID, NAME)
VALUES (
	@ED.customerID, --id
       	'search'--name
      );
"""
    statement1 = """INSERT INTO ENTITY_DEF (ID, ENV_ID, NAME)
VALUES (
\t3, 66, 'customer')"""
    statement2 = """INSERT INTO VERB (ID, NAME)
VALUES (
\t3, 'search')"""

    table = {"ED": {"customerID": 3}, "ENV": {"Dflt": 66}}
    loader = FakeRelativeIdLoader(table)

    assert [statement1, statement2] == SQLParser(loader).parse_runnable_statements(
        sqltext
    )


def test_parse_sql_ended_with_comments_remove_end_comments():
    statement1 = "INSERT INTO VERB(ID,NAME) VALUES(1,'search')"
    sqltext = statement1 + ";\n--some comment"
    loader = FakeRelativeIdLoader(None)
    assert [statement1] == SQLParser(loader).parse_runnable_statements(sqltext)


def run_test_parse_update(expected, query):
    assert expected == SQLParser().parse_update_stmt(query)


def test_parse_update_syntax():
    run_test_parse_update(
        "UPDATE VERB SET NAME='search'", "UPDATE VERB SET (NAME)=('search')"
    )
    run_test_parse_update(
        "UPDATE VERB SET NAME='search'", "UPDATE VERB SET (NAME) = ('search')"
    )
    run_test_parse_update(
        "UPDATE VERB SET ID=1, NAME='search'", "UPDATE VERB SET (ID,NAME)=(1,'search')"
    )

    run_test_parse_update("UPDATE VERB SET ID=1", "UPDATE VERB SET ID=1")
    run_test_parse_update("update VERB SET ID=1", "update VERB SET ID=1")
    update_query = """ UPDATE EVA_CONTEXT_VERB_ENTRY
SET (SEQUENCE_NUMBER) = (2)
where CONFIG_ID = 100
and ENTITY_DEF_TYPE_ID = 2483
and VERB = 'launchCobrowse'
"""
    expected = """ UPDATE EVA_CONTEXT_VERB_ENTRY
SET SEQUENCE_NUMBER = 2
where CONFIG_ID = 100
and ENTITY_DEF_TYPE_ID = 2483
and VERB = 'launchCobrowse'
"""
    run_test_parse_update(update_query, update_query)
    run_test_parse_update("SELECT * FROM VERB", "SELECT * FROM VERB")


def test_does_not_parse_update_syntax_if_already_valid_sql():
    sqltext = """update agent
set PASSWORD = (select PASSWORD from AGENT where username ='admin')
where USERNAME in ('ccagentdemo'); 
"""
    run_test_parse_update(sqltext, sqltext)


def run_extract_set_group(expected, string):
    assert expected == SQLParser().extract_set_group(string)


def test_extract_set_group():
    run_extract_set_group(
        "(ID,NAME)=(1,'search')", "UPDATE VERB SET (ID,NAME)=(1,'search')"
    )
    run_extract_set_group("(ID)=(1)", "UPDATE VERB SET (ID)=(1)")
    run_extract_set_group("(ID)=(1)", "UPDATE VERB SET (ID)=(1) WHERE ID>1")
    run_extract_set_group("(ID)=(1)", "UPDATE VERB SET (ID)=(1) where ID>1")
    run_extract_set_group("(ID)=(1)", "UPDATE VERB set (ID)=(1) where ID>1")


def assert_convert_to_set_clause(expected, string):
    assert expected == SQLParser().convert_set_clause(string)


def test_parse_set_clause():
    assert_convert_to_set_clause("a=b, b=c", "(a,b)=(b,c)")
    assert_convert_to_set_clause("a=b", "(a)=(b)")
