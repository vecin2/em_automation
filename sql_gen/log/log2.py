import os
import yaml

script_dir = os.path.dirname(__file__)
default_path = os.path.join(script_dir, "logging.yaml")
import logging.config
import logging

# import pdb; pdb.set_trace()
def config(prj_root=None):
    path = default_path
    config = {}
    if os.path.exists(path):
        with open(path, "rt") as f:
            content = f.read()
            info_path = os.path.join(prj_root, "logs", "info.log")
            error_path = os.path.join(prj_root, "logs", "error.log")
            content = content.format(info_path=info_path, error_path=error_path)

            config = yaml.safe_load(content)
    return config


def setup_logging(default_path=default_path, app_path=None, default_level=logging.INFO):
    """Setup logging configuration"""
    path = default_path
    if os.path.exists(path):
        with open(path, "rt") as f:
            content = f.read()

            if app_path:
                logs_dir = os.path.join(app_path, "logs")
                if not os.path.exists(logs_dir):
                    os.makedirs(logs)
                info_log_path = os.path.join(logs_dir, "info.log")
            else:
                info_log_path = "info.log"

            content = content.format(
                info_path=info_log_path,
                error_path="/opt/em/projects/GSC/gsc_phase1/logs/error.log",
            )

            config = yaml.safe_load(content)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


setup_logging()
logger = logging.getLogger("app_logger")
