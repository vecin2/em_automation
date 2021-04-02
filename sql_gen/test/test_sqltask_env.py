from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv


def extract_path(env_vars):
    return EMTemplatesEnv().extract_templates_path(env_vars)


def test_when_template_path_set_env_var_returns_it(fs):
    templates_path = "/opt/em/prj/templates"
    env_vars = {"SQL_TEMPLATES_PATH": templates_path}
    fs.create_dir(templates_path)
    path = extract_path(env_vars)
    assert "/opt/em/prj/templates" == path
