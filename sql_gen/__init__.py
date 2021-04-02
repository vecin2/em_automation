import os
from sql_gen.log.log import logger

import pytest

pytest.register_assert_rewrite("sql_gen.commands")
appname = "sqltask"
