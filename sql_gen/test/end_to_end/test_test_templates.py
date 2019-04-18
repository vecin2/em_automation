import pytest

from sql_gen.test.utils.app_runner import TemplatesAppRunner
from sql_gen.commands.verify_templates_cmd import SourceTestBuilder

@pytest.fixture
def app_runner(fs,capsys):
    app_runner = TemplatesAppRunner(fs=fs,capsys=capsys)
    yield app_runner
    app_runner.teardown()


def test_no_test_folder_prints_error(app_runner,fs):
    expected="Test folder '/em/prj/devtask/test_templates' does not exist.\n"
    app_runner.with_emproject_under("/em/prj")\
               .and_prj_built_under("/em/prj")\
               .add_template("greeting.sql","hello {{name}}!")\
               .run()\
               .assert_message_printed(expected)

def test_testname_not_matching_template_does_not_run(app_runner,fs):
    app_runner.with_emproject_under("/em/prj")\
               .and_prj_built_under("/em/prj")\
               .add_template("greeting.sql","hello {{name}}!")\
               .make_test_dir()\
               .add_test("test_bye.sql",{"name":"John"},"hello John!")\
               .run()\
               .generates_no_test()

def test_testname_not_sql_ext_does_not_run(app_runner,fs):
    app_runner.with_emproject_under("/em/prj")\
               .and_prj_built_under("/em/prj")\
               .add_template("greeting.sql","hello {{name}}!")\
               .make_test_dir()\
               .add_test("test_greeting.sqls",{"name":"John"},"hello John!")\
               .run()\
               .generates_no_test()

def test_generates_test_expected_sql(app_runner,fs):
    gen_greeting_test={"tests":"expected-sql",
                       "template_name":"greeting",
                       "expected":"hello John!",
                       "actual":"hello John!"}
    app_runner.with_emproject_under("/em/prj")\
               .and_prj_built_under("/em/prj")\
               .add_template("greeting.sql","hello {{name}}!")\
               .make_test_dir()\
               .add_test("test_greeting.sql",{"name":"John"},"hello John!")\
               .run_test_render_sql()\
               .assert_generate_tests([gen_greeting_test])

def test_generates_multiple_test_expected_sql(app_runner,fs):
    gen_hello_test={"tests":"expected-sql",
                       "template_name":"hello",
                       "expected":"hello Fred!",
                       "actual":"hello Fred!"}
    gen_bye_test={"tests":"expected-sql",
                       "template_name":"bye",
                       "expected":"bye Mark!",
                       "actual":"bye Mark!"}
    app_runner.with_emproject_under("/em/prj")\
               .and_prj_built_under("/em/prj")\
               .add_template("hello.sql","hello {{name}}!")\
               .add_template("bye.sql","bye {{name}}!")\
               .make_test_dir()\
               .add_test("test_hello.sql",{"name":"Fred"},"hello Fred!")\
               .add_test("test_bye.sql",{"name":"Mark"},"bye Mark!")\
               .run_test_render_sql()\
               .assert_generate_tests([gen_hello_test,gen_bye_test])

def test_generates_single_test_run_query(app_runner,fs):
    gen_verb_test={"tests":"run-on-db",
                   "template_name":"verb",
                   "query":"select name from verb",
                   "emprj_path":"/em/prj"}
    app_runner.with_emproject_under("/em/prj")\
               .and_prj_built_under("/em/prj")\
               .add_template("verb.sql","select {{column}} from verb")\
               .make_test_dir()\
               .add_test("test_verb.sql",{"column":"name"},"select name from verb")\
               .run_test_with_db()\
               .assert_generate_tests([gen_verb_test])
