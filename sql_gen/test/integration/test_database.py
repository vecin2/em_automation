from sql_gen.emproject import addb,current_emproject

def test_addb():
    #current_emproject.clear_config()
    result  =addb().query("SELECT * FROM EVA_ENTITY_DEFINITION WHERE NAME = 'CustomerED'")
    assert len(result) >0
    assert "CustomerED"==result[0]['NAME']
