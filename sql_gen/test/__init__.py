import pytest

pytest.register_assert_rewrite("sql_gen.test.utils.app_runner")
pytest.register_assert_rewrite("sql_gen.test.utils.db_utils")
pytest.register_assert_rewrite("sql_gen.test.utils.prompt_builder")
pytest.register_assert_rewrite("devtask.extend_process")
