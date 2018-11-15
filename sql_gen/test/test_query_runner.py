import pytest
from sql_gen.emproject import QueryRunner
from sql_gen.exceptions import ConfigFileNotFoundException

class  FakeEMDB():
    def __init__(self):
        self.list_query=""
        self.find_query=""
    def list(self, query):
        self.list_query = query
    def find(self, query):
        self.find_query = query

def test_list_calls_list_in_db_with_correct_query():
    fakedb = FakeEMDB()
    queries ={"v__by_name":"SELECT * FROM verb_name WHERE NAME='{}' and IS_DELETED='{}'"}
    ad=QueryRunner(queries,fakedb)
    ad.list.v__by_name("inlineSearch","N")

    expected_query = "SELECT * FROM verb_name WHERE NAME='inlineSearch' and IS_DELETED='N'"
    assert expected_query== fakedb.list_query

def test_find_calls_find_in_db_with_correct_query():
    fakedb = FakeEMDB()
    queries ={"v__by_id":"SELECT * FROM EVA_VERB WHERE ID =123"}
    ad=QueryRunner(queries,fakedb)
    ad.find.v__by_id("inlineSearch","N")

    expected_query = "SELECT * FROM EVA_VERB WHERE ID =123"
    assert expected_query== fakedb.find_query

def test_make_queries_from_file(fs):
    file_content="""
v__by_name=SELECT * FROM verb_name WHERE NAME='{}' and IS_DELETED='{}'
"""
    expected_dict ={"v__by_name":"SELECT * FROM verb_name WHERE NAME='{}' and IS_DELETED='{}'"}
    file_path="/em/gsc/queries.sql"
    fs.create_file(file_path,contents=file_content)

    ad=QueryRunner.make_from_file(file_path,None)

    assert expected_dict == ad.query_dict

def test_make_queries_from_file_throws_exception_if_file_not_exist():
    with pytest.raises(ConfigFileNotFoundException) as exc_info:
        ad=QueryRunner.make_from_file("/queries.sql",None)

    assert "queries.sql" in str(exc_info.value)

