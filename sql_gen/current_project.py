from sql_gen.app_project import AppProject
from sql_gen.emproject import EMProject

app = AppProject(EMProject())
logger  = app.get_logger()
logger.info("Initializing app which is pointing currently to '"+app.emproject.root+"'")



