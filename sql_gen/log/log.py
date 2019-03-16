import os
import logging.config
import yaml

def basic_setup(logs_dir="."):
    return logging.config.dictConfig(basic_config(logs_dir))

def basic_config(logs_dir="."):
    default_config = _get_content(default_config_file())
    content = _replace_logs_dir(default_config, logs_dir)
    return yaml.safe_load(content)

def _get_content(config_file):
    with open(config_file, 'rt') as f:
        return f.read()

def setup_from_file(config_file=None):
    return logging.config.dictConfig(file_config(config_file))

def file_config(config_file):
    return yaml.safe_load(_get_content(config_file))

def default_config_file():
    script_dir =os.path.dirname(__file__)
    return os.path.join(script_dir,"logging.yaml")

def _replace_logs_dir(default_config,logs_dir):
    info_path = os.path.join(logs_dir,"info.log")
    error_path = os.path.join(logs_dir,"error.log")
    return default_config.format(info_path=info_path,
                             error_path=error_path)

def set_logger(logger_arg):
    logger = logger_arg

logger = logging.getLogger("app_logger")
