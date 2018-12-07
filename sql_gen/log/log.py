import os
import logging.config
import yaml


def _get_config_file_path(root):
    prj_config =os.path.join(root,"config","logging.yaml")
    if os.path.exists(prj_config):
        return  prj_config
    else:
        script_dir =os.path.dirname(__file__)
        return os.path.join(script_dir,"logging.yaml")

def _read_default_config_and_render_vars(path,prj_root):
    content =""
    if os.path.exists(path):
        with open(path, 'rt') as f:
            content =f.read()
            info_path = os.path.join(prj_root,"logs","info.log")
            error_path = os.path.join(prj_root,"logs","error.log")
            content = content.format(info_path=info_path,
                                     error_path=error_path)
    return content

def config(prj_root=None):
    path = _get_config_file_path(prj_root)
    content = _read_default_config_and_render_vars(path,prj_root)
    return yaml.safe_load(content)

def setup_logging(prj_root=None):
    config_dict =config(prj_root)
    logging.config.dictConfig(config_dict)

logger = logging.getLogger("app_logger")

