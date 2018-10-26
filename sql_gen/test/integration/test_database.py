from sql_gen.emproject import addb,current_emproject

def test_addb():
    current_emproject.clear_config()
    addb().query("SELECT * FROM EVA_ENTITY_DEFINITION")
