from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    """
    Base model for Post with common attributes.
    """
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    """
    Model for creating a new post. Inherits all fields from PostBase.
    """
    pass

class UserOut(BaseModel):
    """
    Model for user output, excluding sensitive information like password.
    """
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True  # Allows the model to read data from ORM objects

class Post(PostBase):
    """
    Complete Post model, including database fields and owner information.
    """
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    """
    Model for post output, including vote count.
    """
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    """
    Model for creating a new user.
    """
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """
    Model for user login credentials.
    """
    email: EmailStr
    password: str

class Token(BaseModel):
    """
    Model for authentication token.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Model for token payload data.

    """
    id: Optional[str] = None

class Upvote(BaseModel):
    """
    Model for upvoting a post.
    dir: 1 for upvote, 0 for removing upvote
    """
    post_id: int
    dir: conint(le=1)  # Constrained integer, less than or equal to 1
