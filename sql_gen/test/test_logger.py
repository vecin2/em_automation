import pytest
import sql_gen.logger.log as log


def test_log_path_comes_from_config(fs):
    log_file_path="log.log"
    config ={"LOG_FILE":log_file_path}
    logger =log.get_logger("session")
    message ="test log file path"
    logger.info(message)
    with open(log_file_path, 'r') as content_file:
        content = content_file.read()
    assert message == content

