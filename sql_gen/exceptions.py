
class DBConnectionException(Exception):
    """This exception is raised when unable to connect to database.
    """
class CCAdminException(Exception):
    """This exception is raised when ccadmin command failed
    """
class ConfigFileNotFound(Exception):
    """This exception is raised when reading configuration file but the file does not exists.
    """
