from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class Post(Base):
    """
    Represents a post in the application.

    Attributes:
        id (int): The unique identifier for the post.
        title (str): The title of the post.
        content (str): The content of the post.
        published (bool): Whether the post is published or not.
        created_at (datetime): The timestamp when the post was created.
        owner_id (int): The ID of the user who created the post.
        owner (User): The relationship to the User who owns this post.
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    """
    Represents a user in the application.

    Attributes:
        id (int): The unique identifier for the user.
        email (str): The email address of the user (unique).
        password (str): The hashed password of the user.
        created_at (datetime): The timestamp when the user account was created.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Upvote(Base):
    """

    Represents an upvote in the application.

    This is a join table that connects users to posts they've upvoted.

    Attributes:
        user_id (int): The ID of the user who made the upvote.
        post_id (int): The ID of the post that was upvoted.
    """
    __tablename__ = "upvotes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)
