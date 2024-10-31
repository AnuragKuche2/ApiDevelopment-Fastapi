from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Configuration settings for the application.

    This class uses Pydantic's BaseSettings to manage configuration variables.
    It automatically reads these variables from environment variables or a .env file.

    Attributes:
        database_hostname (str): Hostname of the database server
        database_port (str): Port number for the database connection
        database_password (str): Password for database authentication
        database_name (str): Name of the database to connect to
        database_username (str): Username for database authentication
        secret_key (str): Secret key used for cryptographic signing
        algorithm (str): Algorithm used for token encoding/decoding
        access_token_expire_minutes (int): Expiration time for access tokens in minutes

    The Config class within Settings specifies that these settings should be read from a .env file.

    """

    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

# Create an instance of the Settings class
# This will load the configuration from environment variables or the .env file
settings = Settings()
