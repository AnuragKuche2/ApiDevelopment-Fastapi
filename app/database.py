# Import necessary modules from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import psycopg2 for PostgreSQL database connection
import psycopg2
from psycopg2.extras import RealDictCursor

# Import time module for potential connection retry delays
import time

# Import settings from local config file
from .config import settings

# Construct the database URL using settings
# Format: postgresql://<username>:<password>@<hostname>:<port>/<database_name>
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create SessionLocal class
# autocommit=False: Transactions are not automatically committed
# autoflush=False: Changes are not automatically flushed to the database
# bind=engine: Bind the session to our database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()

def get_db():
    """
    Generator function to get a database session.
    This function creates a new SQLAlchemy SessionLocal that will be used in a single request,
    and then closed once the request is finished.

    Yields:
        SessionLocal: A SQLAlchemy ORM session

    Usage:
        This function is typically used with FastAPI's dependency injection system.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Note: The following is an example of how you might set up a direct connection using psycopg2
# This code is currently commented out, but could be used if needed for direct database operations

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                                 password='password123', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)
