from sql_gen.app_project import AppProject
from sql_gen.emproject import EMProject
from sql_gen.logger.log import setup_logging
import os

app = AppProject(EMProject())
setup_logging(os.path.join(app.paths["config"],"logging.yaml"))
logger  = app.get_logger()
logger.info("Initializing app which is pointing currently to '"+app.emproject.root+"'")



