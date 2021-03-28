from sql_gen.commands.verify_templates_cmd import RunOnDBTestTemplate


# test were failing when windows folde like \trunk or \Users
def test_runondb_template():
    template = RunOnDBTestTemplate()
    emprj_path = "c:\em\projects\\trunk"
    repr_path = repr(emprj_path)
    result = template.render(query="query", emprj_path=emprj_path).to_string()
    assert repr_path in result
