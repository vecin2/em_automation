from sql_gen.emproject import addb,current_emproject
import pytest

#@pytest.mark.skip
def test_addbquery():
    #current_emproject.clear_config()
    result  =addb().query("SELECT * FROM EVA_ENTITY_DEFINITION WHERE NAME = 'CustomerED'")
    assert len(result) >0
    assert "CustomerED"==result[0]['NAME']
def test_addblist():
    #current_emproject.clear_config()
    result  =addb().list("SELECT NAME  FROM EVA_ENTITY_DEFINITION WHERE NAME = 'CustomerED'")
    assert len(result) >0
    assert "CustomerED"==result[0]
