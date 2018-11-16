from sql_gen.app_project import AppProject
from sql_gen.emproject import EMProject
from sql_gen.logger import logger


app = AppProject(EMProject())
logger.info("Initializing app which is pointing currently to '"+app.emproject.root+"'")


