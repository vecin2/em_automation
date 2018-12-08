from sql_gen.app_project import AppProject
from sql_gen.emproject import EMProject
from sql_gen.log.handlers import MakeRotatingFileHandler
import os

app = AppProject(EMProject())
#os.path.join(app.paths["config"],"logging.yaml")
logger  = app.get_logger()
logger.info("Initializing app which is pointing currently to '"+app.emproject.root+"'")



