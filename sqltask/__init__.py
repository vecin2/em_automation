import os
from sqltask.log.log import logger

import pytest

pytest.register_assert_rewrite("sqltask.commands")
appname = "sqltask"
