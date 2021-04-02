import pytest
from sql_gen.emproject import QueryRunner
from sql_gen.exceptions import ConfigFileNotFoundException


class FakeEMDB:
    def __init__(self):
        self.fetch_query = ""
        self.find_query = ""

    def pop_fetch_query(self):
        result = self.fetch_query
        self.fetch_query = ""
        return result

    def fetch(self, query):
        self.fetch_query = query

    def find(self, query):
        self.find_query = query


queries = {
    "v__by_name": "SELECT * FROM verb_name WHERE NAME='{}' and IS_DELETED='{}'",
    "v__by_name_with_keywords": "SELECT * FROM verb_name WHERE NAME='{name}' and IS_DELETED='{deleted}'",
}


@pytest.mark.parametrize("op_name", ["fetch", "find"])
def test_run_query_call_db_with_correct_query(op_name):
    fakedb = FakeEMDB()
    ad = QueryRunner(query_dict=queries, emdb=fakedb)
    op = getattr(ad, op_name)  # ad.fetch or ad.find
    op.v__by_name_with_keywords(name="inlineSearch", deleted="N")

    expected_query = (
        "SELECT * FROM verb_name WHERE NAME='inlineSearch' and IS_DELETED='N'"
    )
    assert expected_query == fakedb.__getattribute__(op_name + "_query")


@pytest.mark.parametrize("op_name", ["fetch", "find"])
def test_run_query_with_wrong_number_args_throws_exception(op_name):
    fakedb = FakeEMDB()
    ad = QueryRunner(query_dict=queries, emdb=fakedb)
    with pytest.raises(AssertionError) as excinfo:
        op = getattr(ad, op_name)  # ad.fetch or ad.find
        op.v__by_name("inlineSearch")
    assert "Method 'v__by_name' takes 2 params (1 given)" == str(excinfo.value)
    assert "" == fakedb.pop_fetch_query()


@pytest.mark.parametrize("op_name", ["fetch", "find"])
def test_non_existing_throws_exception_no_query_defined(op_name):
    fakedb = FakeEMDB()
    ad = QueryRunner(queries, fakedb)
    with pytest.raises(AssertionError) as excinfo:
        op = getattr(ad, op_name)  # ad.fetch or ad.find
        op.something_else("inlineSearch")
    assert "No query defined called 'something_else'." == str(excinfo.value)
    assert "" == fakedb.pop_fetch_query()


@pytest.mark.parametrize("op_name", ["fetch", "find"])
def test_non_existing_query_with_similar_name_throws_exception_suggest_queries(op_name):
    fakedb = FakeEMDB()
    ad = QueryRunner(query_dict=queries, emdb=fakedb)
    with pytest.raises(AssertionError) as excinfo:
        op = getattr(ad, op_name)  # ad.fetch or ad.find
        op.v__by_nam("inlineSearch")
    assert (
        "No query defined called 'v__by_nam'. Did you mean?\nv__by_name\nv__by_name_with_keywords"
        == str(excinfo.value)
    )
    assert "" == fakedb.pop_fetch_query()


def test_make_queries_from_file(fs):
    file_content = """
v__by_name=SELECT * FROM verb_name WHERE NAME='{}' and IS_DELETED='{}'
"""
    expected_dict = {
        "v__by_name": "SELECT * FROM verb_name WHERE NAME='{}' and IS_DELETED='{}'"
    }
    file_path = "/em/gsc/queries.sql"
    fs.create_file(file_path, contents=file_content)

    ad = QueryRunner.make_from_file(file_path, db=FakeEMDB())

    assert expected_dict == ad.query_dict.properties


def test_run_query_does_throws_exception_if_file_not_exist():
    with pytest.raises(FileNotFoundError) as excinfo:
        ad = QueryRunner.make_from_file("/queries.sql", db=FakeEMDB())
        ad.fetch.my_query()
    assert "Try to load config file '/queries.sql' but it does not exist" in str(
        excinfo
    )


def test_something():
    fakedb = FakeEMDB()
    query_runner = QueryRunner(query_dict=queries, emdb=fakedb)
    query_runner.find.v__by_name
    assert fakedb == query_runner.addb
