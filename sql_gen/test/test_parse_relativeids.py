from sql_gen.database.sqlparser import RelativeId, RelativeIdReplacer,SQLParser


class FakeRelativeIdLoader(object):
    def __init__(self,storage_table=None):
        self.storage_table =storage_table
    def load(self,keyset,keyname):
        return self.storage_table[keyset][keyname]

def assert_relative_ids(expected_list, sqltext):
    assert expected_list == RelativeIdReplacer().find_all(sqltext)

def test_matching_relative_ids():
    assert_relative_ids([],"@CC.Home)")
    assert_relative_ids(["@CC.Home"],"(@CC.Home)")
    assert_relative_ids(["@CC.Home"],",@CC.Home)")
    assert_relative_ids(["@CC.Home"]," @CC.Home)")
    assert_relative_ids(["@CC.Home"],"'frank.smith@gmail.com',@CC.Home)")
    assert_relative_ids(["@CC.Home"]," @CC.Home,@CC.Home")


def assert_replace_ids(replacer,expected,sqltext):
    assert expected == replacer.replace(sqltext)

def test_replace_ids():
    table = {"CC": {"Home": 123, "Admin":234},
             "ED": {"Agent": 345, "ContactHistory": 567}
            }
    loader = FakeRelativeIdLoader(storage_table=table)
    replacer = RelativeIdReplacer(loader)
    assert_replace_ids(replacer,"(123)","(@CC.Home)")
    assert_replace_ids(replacer,"(123,123)","(@CC.Home,@CC.Home)")
    assert_replace_ids(replacer,"(123,234,345,567)","(@CC.Home,@CC.Admin,@ED.Agent,@ED.ContactHistory)")

def test_remove_comments_and_strip_str():
    sqltext=""" INSERT INTO VERB(ID,NAME)
    VALUES(12, --id
           "search" --name
           ) """
    expected="""INSERT INTO VERB(ID,NAME)
    VALUES(12, "search"  )"""
    assert expected == SQLParser().strip_comments(sqltext)

def test_splits_multiple_runnable_stmts():
    sqltext="""SELECT * FROM VERB;
    SELECT * FROM ENTITY;"""
    stmt1="SELECT * FROM VERB"
    stmt2="SELECT * FROM ENTITY"
    assert [stmt1,stmt2]==SQLParser().split(sqltext)

def test_parse_full_sql():
    sqltext="""
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
    statement1 ="""INSERT INTO ENTITY_DEF (ID, ENV_ID, NAME)
VALUES (
\t3, 66, 'customer')"""
    statement2 ="""INSERT INTO VERB (ID, NAME)
VALUES (
\t3, 'search')"""

    table = {"ED": {"customerID": 3},
             "ENV": {"Dflt": 66}
            }
    loader = FakeRelativeIdLoader(table)

    assert [statement1, statement2] == SQLParser(loader).parse_runnable_statements(sqltext)

