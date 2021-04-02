class CCAdminException(Exception):
    """This exception is raised when ccadmin command failed"""


class ConfigFileNotFoundException(Exception):
    """This exception is raised when reading configuration file but the file does not exists."""


class EnvVarNotFoundException(Exception):
    """Raised when an expect environment variable is not set"""

    def __init__(self, env_name, help_text):
        super().__init__(
            "'" + env_name + "' is not set within environment variables. " + help_text
        )


class InvalidEnvVarException(Exception):
    """Raised when a envrionment variable is set but to a wrong value"""


class InvalidFileSystemPathException(Exception):
    """Raised when a envrionment variable is set but to a wrong value"""


class ConfigException(Exception):
    """This exception is raised when unable to configure EM, usually because ccadmin run failed"""


class IllegalArgumentError(ValueError):
    """When invoking a method with the wrong number of arguments"""


class DatabaseError(ValueError):
    """Error when connecting with database"""
