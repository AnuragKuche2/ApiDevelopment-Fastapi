# Import necessary modules from FastAPI and other dependencies
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

# Create an APIRouter instance for user-related routes
router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    This function handles user registration. It hashes the user's password
    before storing it in the database for security purposes.

    Args:
        user (schemas.UserCreate): The user data to be created
        db (Session): The database session

    Returns:
        models.User: The created user object

    Raises:
        HTTPException: If there's an error during user creation
    """

    # Hash the password for security
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # Create a new User model instance and add it to the database
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by their ID.

    This function fetches a user from the database based on the provided ID.

    Args:
        id (int): The ID of the user to retrieve
        db (Session): The database session
    Returns:
        models.User: The user object if found

    Raises:
        HTTPException: If the user with the given ID is not found
    """

    # Query the database for the user with the given ID
    user = db.query(models.User).filter(models.User.id == id).first()

    # If user not found, raise a 404 Not Found exception
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user
