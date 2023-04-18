from sql_gen.emproject.config import EMConfigID
from sql_gen.test.config.utils import PropertiesFolderGenerator


class EMEnvironmentConfigGenerator(PropertiesFolderGenerator):
    def __init__(self, env_name=None, machine_name=None):
        super().__init__()
        self.env_name = env_name
        self.machine_name = machine_name
        self.config_path = None

    def generate_config(self):
        # same api as ccadmin client
        return self.save(self.config_path)

    def _get_file_name(self, key):
        return EMConfigID(self.env_name, self.machine_name, key).filename()
