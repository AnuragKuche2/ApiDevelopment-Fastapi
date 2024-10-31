from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base

# Define the database URL for testing
# Note: The hardcoded URL is commented out in favor of using environment variables
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

# Create a new SQLAlchemy engine instance for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a TestingSessionLocal class for creating database sessions
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


# Fixture to create a fresh database session for each test
@pytest.fixture()
def session():
    # Drop all tables in the test database
    Base.metadata.drop_all(bind=engine)
    # Create all tables in the test database
    Base.metadata.create_all(bind=engine)
    # Create a new session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Fixture to create a test client with a database session
@pytest.fixture()
def client(session):
    # Dependency override to use the test database session
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    # Override the get_db dependency in the app
    app.dependency_overrides[get_db] = override_get_db

    # Create and return a TestClient instance
    yield TestClient(app)
