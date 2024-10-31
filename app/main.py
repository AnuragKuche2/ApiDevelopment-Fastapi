import psycopg2
from fastapi import FastAPI, Response, status, HTTPException
from .routers import upvote, post, user, auth

import time
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from .config import settings

# Initialize FastAPI application
app = FastAPI()

# Define Post model using Pydantic
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Attempt to connect to the PostgreSQL database
while True:
    try:
        conn = psycopg2.connect(
            host=settings.DATABASE_HOSTNAME,
            database=settings.DATABASE_NAME,
            user=settings.DATABASE_USERNAME,
            password=settings.DATABASE_PASSWORD,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print('Database connection was successful')
        break
    except Exception as error:
        print('Connection failed')
        print(f"error was {error}")
        time.sleep(2)

# Sample data (to be replaced with database operations)
my_posts = [
    {'title': "title of post 1", "content": "content of first post", "id": 1},
    {'title': "title of post 2", "content": "content of second post", "id": 2}
]

# Helper function to find a post by id
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

# Helper function to find the index of a post by id
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

# Include routers from other modules
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(upvote.router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Hello World, welcome to fastapi"}

# Get all posts
@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

# Create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    print(post.content)
    print(post.title)
    print(post.published)
    return {"data": post}

# Get a specific post by id
@app.get("/posts/{id}")
async def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_details": f"This is the post {id} you have requested for"}

# Delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post
@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"message": post_dict}
