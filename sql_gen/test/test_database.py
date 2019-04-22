from sql_gen.database import EMDatabase
from sql_gen.test.utils.db_utils import FakeDBConnector
import pytest


def test_find_throws_exception_if_more_than_one_found():
    fake_cursor =[("ID", "NAME"),
             (1,"inlineCreate"),
             (2,"inlineSearch")
            ]
    fake_conn = FakeDBConnector(fake_cursor)
    fake_db = EMDatabase(fake_conn)

    with pytest.raises(LookupError) as e_info:
        fake_db.find("SELECT * FROM VERB")
    assert "Expected to find one record but query 'SELECT * FROM VERB' returned None or more than one. If you expect more that one record use fetch instead" == str(e_info.value)

def test_find_returns_when_only_one_result_is_returned():
    fake_cursor =[("ID", "NAME"),
             (1,"inlineCreate")
            ]
    fake_conn = FakeDBConnector(fake_cursor)
    fake_db = EMDatabase(fake_conn)
    result =fake_db.find("")
    assert 1 == result["ID"]
    assert "inlineCreate" == result["NAME"]


def test_list_will_return_a_list_of_items_in_the_first_column():
    fake_cursor =[("ID", "NAME"),
             (1,"inlineCreate"),
             (2,"inlineSearch")
            ]
    fake_conn = FakeDBConnector(fake_cursor)
    fake_db = EMDatabase(fake_conn)

    query ="SELECT * FROM CCADMIN_IDMAP"
    result = fake_db.list(query)
    assert 2 ==len(result)
    assert 1 == result[0]
    assert 2 == result[1]

