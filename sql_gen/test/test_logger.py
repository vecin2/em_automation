import pytest
from sql_gen.app_project import AppProject
from sql_gen.emproject import EMProject
#from sql_gen.loggu import log
from sql_gen.logger import log

@pytest.mark.skip
def test_log_path_comes_from_config(fs):
    log_file_path="log.log"
    config ={"LOG_FILE":log_file_path}
    logger =log.get_logger("session")
    message ="test log file path"
    logger.info(message)
    with open(log_file_path, 'r') as content_file:
        content = content_file.read()
    assert message == content

def test_default_log_config():
    root =  "/my_project/sqltask"
    import pdb; pdb.set_trace()
    config = log.config(root)

    info_log_path =config['handlers']['info_file_handler']['filename']
    error_log_path =config['handlers']['error_file_handler']['filename']
    assert "/my_project/sqltask/logs/info.log" == info_log_path
    assert "/my_project/sqltask/logs/error.log" == error_log_path

