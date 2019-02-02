from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv

def get_templates_path(env_vars):
    return EMTemplatesEnv().get_templates_path(env_vars)

def test_list_templates_from_sql_templates_path():
    env_vars={"SQL_TEMPLATES_PATH":"/opt/sqltask/templates"}

    templates_path = get_templates_path(env_vars)
    assert "/opt/sqltask/templates" == templates_path


def test_sql_template_path_not_set_computes_loc_from_em_core_home():
    env_vars={"EM_CORE_HOME":"/opt/my_project"}

    templates_path = get_templates_path(env_vars)

    assert "/opt/my_project/sqltask/templates" == templates_path




