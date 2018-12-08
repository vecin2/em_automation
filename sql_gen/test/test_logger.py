import pytest
from sql_gen.app_project import AppProject
from sql_gen.emproject import EMProject
#from sql_gen.loggu import log
from sql_gen.log import log

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

def test_basic_config():
    logs_dir =  "/my_project/sqltask/logs"
    config = log.basic_config(logs_dir)

    info_log_path =config['handlers']['info_file_handler']['filename']
    error_log_path =config['handlers']['error_file_handler']['filename']
    assert "/my_project/sqltask/logs/info.log" == info_log_path
    assert "/my_project/sqltask/logs/error.log" == error_log_path

def test_file_config(fs):
    log_config_file =  "/my_project/sqltask/config/logging.yaml"
    fs.create_file(log_config_file,contents=config_content)
    config = log.file_config(log_config_file)

    info_log_path =config['handlers']['info_file_handler']['filename']
    assert "information.log" == info_log_path

config_content="""
version: 1
disable_existing_loggers: False
formatters:
    simple:
        format: "%(asctime)s - %(levelname)s - %(message)s"

handlers:
    info_file_handler:
        class: sql_gen.log.handlers.MakeRotatingFileHandler
        level: INFO
        formatter: simple
        filename: information.log
        maxBytes: 10485760 # 10MB
        backupCount: 20
        encoding: utf8
loggers:
    app_logger:
        level: INFO
        handlers: [console,info_file_handler, error_file_handler]
        propagate: no

root:
    level: INFO
    handlers: [console, info_file_handler, error_file_handler]
"""
