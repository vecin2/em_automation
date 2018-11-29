import os
import logging.config
import yaml

script_dir =os.path.dirname(__file__)
default_path=os.path.join(script_dir,"logging.yaml")

def config(prj_root=None):
    path = default_path
    config ={}
    if os.path.exists(path):
        with open(path, 'rt') as f:
            content =f.read()
            info_path = os.path.join(prj_root,"logs","info.log")
            error_path = os.path.join(prj_root,"logs","error.log")
            content = content.format(info_path=info_path,
                                     error_path=error_path)

            config = yaml.safe_load(content)
    return config

def setup_logging(prj_root=None):
    config_dict =config(prj_root)
    logging.config.dictConfig(config_dict)

logger = logging.getLogger("app_logger")

