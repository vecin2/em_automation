
class DBConnectionException(Exception):
    """This exception is raised when unable to connect to database.
    """
class CCAdminException(Exception):
    """This exception is raised when ccadmin command failed
    """
class ConfigFileNotFoundException(Exception):
    """This exception is raised when reading configuration file but the file does not exists.
    """
class EnvironmentVarNotFoundException(Exception):
    def __init__(self,env_name, help_text):
        super().__init__("'"+env_name +"' is not set within environment variables. This var "+ help_text)
class NoDefaultEnvFoundException(Exception):
    """This exception is raised when trying to access to a EM project configuration but there is no default environent setup. In this case EMProject does not know for which of its environments return the config"""

class ConfigException(Exception):
    """This exception is raised when unable to configure EM, usually because ccadmin run failed
    """
