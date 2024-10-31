# Import necessary modules from FastAPI
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Import custom modules
from .. import database, schemas, models, utils, oauth2

# Create an APIRouter instance for authentication routes
router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """

    Authenticate user and create access token.

    Args:
        user_credentials (OAuth2PasswordRequestForm): Form containing username and password.
        db (Session): Database session.

    Returns:
        dict: Contains access token and token type.

    Raises:
        HTTPException: 403 error if credentials are invalid.
    """

    # Query the database for the user with the provided email
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    # If user not found, raise 403 Forbidden error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # Verify the provided password against the stored hashed password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # Create access token with user ID as payload
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # Return the access token and token type
    return {"access_token": access_token, "token_type": "bearer"}
