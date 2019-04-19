import re

import sqlparse

def load_id(keyset,keyname):
    return 123
sql_txt="INSERT INTO CONTEXT (CONFIG_ID,CONFIG_ENV_ID,VERB,ENTITY_DEF_TYPE_ID,ENTITY_DEF_TYPE_ENV_ID,SEQUENCE_NUMBER,RELEASE_ID) VALUES (\
             @CC.Home, @ENV.Dflt, launchIdentifyPlanMember, @ET.Agent, @ENV.Dflt, 1, @RELEASE.ID  );"
def parse(string):
    return string


class RelativeId(object):
    relativeid_exp="(?<=[^\w])@\w*\.\w*"
    def __init__(self,string,loader=None):
        self.string = string
        self.loader =loader

    @property
    def keyset(self):
        return self.string.split(".")[0][1:]

    @property
    def keyname(self):
        return self.string.split(".")[1]

    def real_id(self):
        return str(self.loader.load(self.keyset,self.keyname))

    def swap_with_realid(self, sql_text):
        return sql_text.replace(self.string,self.real_id())
    def replace_all_instances(self,sql_text):
        return sql_text.replace(self.string,self.real_id())
    @staticmethod
    def parse_all(sql_text):
        return re.findall(RelativeId.relativeid_exp,sql_text)

class RelativeIdLoader(object):
    def __init__(self,storage_table=None):
        self.storage_table =storage_table
    def load(self,keyset,keyname):
        return self.storage_table[keyset][keyname]

class RelativeIdReplacer(object):
    def __init__(self,loader=None):
        self.loader = loader
    REG_EXP="(?<=[^\w])@\w*\.\w*"
    def find_all(self,sql_text):
        ids =re.findall(self.REG_EXP,sql_text)
        #remove duplicates
        return list(set(ids))

    def replace(self,sql_text):
        relative_ids = self.find_all(sql_text)
        for str_relative_id in relative_ids:
            relative_id = RelativeId(str_relative_id,loader=self.loader)
            sql_text = relative_id.replace_all_instances(sql_text)
        return sql_text


def assert_relative_ids(expected_list, sql_text):
    assert expected_list == RelativeIdReplacer().find_all(sql_text)

def test_matching_relative_ids():
    assert_relative_ids([],"@CC.Home)")
    assert_relative_ids(["@CC.Home"],"(@CC.Home)")
    assert_relative_ids(["@CC.Home"],",@CC.Home)")
    assert_relative_ids(["@CC.Home"]," @CC.Home)")
    assert_relative_ids(["@CC.Home"],"'frank.smith@gmail.com',@CC.Home)")
    assert_relative_ids(["@CC.Home"]," @CC.Home,@CC.Home")


def assert_replace_ids(replacer,expected,sql_text):
    assert expected == replacer.replace(sql_text)

def test_replace_ids():
    table = {"CC": {"Home": 123, "Admin":234},
             "ED": {"Agent": 345, "ContactHistory": 567}
            }
    loader = RelativeIdLoader(table)
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

class SQLParser(object):
    def __init__(self,loader=None):
        self.relativeId_replacer = RelativeIdReplacer(loader)

    def strip_comments(self,sqltext):
        return sqlparse.format(sqltext,strip_comments=True).strip()

    def split(self,sqltext):
        result =[]
        for statement in sqlparse.split(sqltext):
            #remove semicolon - otherwise throws exc when run
            if statement and statement[-1:]==";":
                statement = statement[:-1]
            result.append(statement)
        return result

    def parse_runnable_statements(self,sqltext):
        sqltext = self.relativeId_replacer.replace(sqltext)
        sqltext = self.strip_comments(sqltext)
        return self.split(sqltext)

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
    loader = RelativeIdLoader(table)

    assert [statement1, statement2] == SQLParser(loader).parse_runnable_statements(sqltext)
def test_replace():
    sql_txt="INSERT INTO CONTEXT (CONFIG_ID) VALUES (@CC.Home);"
    expected="INSERT INTO CONTEXT (CONFIG_ID) VALUES (123);"
