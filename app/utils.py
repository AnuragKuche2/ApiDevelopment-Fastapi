from passlib.context import CryptContext

# Create a CryptContext instance for password hashing
# This uses bcrypt as the hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    """
    Hash a password using bcrypt.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    """
    Verify a plain text password against a hashed password.
    Args:
        plain_password (str): The plain text password to be verified.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
