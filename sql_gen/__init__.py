import os
from sql_gen.emproject import EMConfigID,EMProject
from sql_gen.config import ConfigFile 
from sql_gen.current_project import app

current_emproject=EMProject()
config_path=os.path.join(current_emproject.root,"config/em_automation.properties")
current_config=ConfigFile(config_path)
default_config_id=EMConfigID(current_config["environment.name"],
                             current_config["machine.name"],
                             current_config["container.name"])
current_emproject.set_default_config_id(default_config_id)
