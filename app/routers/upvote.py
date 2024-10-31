# Import necessary modules from FastAPI and other dependencies
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

# Create an APIRouter instance for upvote-related routes
router = APIRouter(
    prefix="/Upvote",
    tags=['Upvote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def Upvote(Upvote: schemas.Upvote, db: Session = Depends(database.get_db),
           current_user: int = Depends(oauth2.get_current_user)):
    """

    Handle upvoting and removing upvotes for posts.

    This function allows users to upvote a post or remove their upvote.
    It checks for the existence of the post and prevents duplicate upvotes.

    Args:
        Upvote (schemas.Upvote): The upvote data (post_id and direction)
        db (Session): The database session
        current_user (int): The authenticated user's ID

    Returns:
        dict: A message indicating the result of the operation

    Raises:
        HTTPException: For various error conditions (404 Not Found, 409 Conflict)
    """

    # Check if the post exists
    post = db.query(models.Post).filter(models.Post.id == Upvote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {Upvote.post_id} does not exist")

    # Query to check if the user has already upvoted this post
    upvote_query = db.query(models.Upvote).filter(
        models.Upvote.post_id == Upvote.post_id, models.Upvote.user_id == current_user.id)

    found_vote = upvote_query.first()

    if (Upvote.dir == 1):
        # User is trying to upvote
        if found_vote:
            # User has already upvoted this post
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {Upvote.post_id}")

        # Create new upvote
        new_vote = models.Upvote(post_id=Upvote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        # User is trying to remove their upvote
        if not found_vote:
            # User hasn't upvoted this post
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Upvote does not exist")

        # Remove the upvote
        upvote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted upvote"}
