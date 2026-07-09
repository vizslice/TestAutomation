"""
Simple FastAPI REST Backend
============================
FastAPI is a modern Python web framework for building APIs quickly.
It automatically generates interactive docs at http://127.0.0.1:8000/docs

Run with:
    uvicorn main:app --reload

Then set Postman baseUrl environment variable to: http://127.0.0.1:8000
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# FastAPI() creates the application instance - this is the core of your API
app = FastAPI(title="Posts API", description="A simple posts API for testing with Postman")

# Pydantic model defines the shape/validation of incoming request data
class Post(BaseModel):
    title: str
    body: str
    userId: int

# In-memory storage - acts like a simple database (resets when server restarts)
posts: dict = {
    1: {"id": 1, "title": "Sample Post", "body": "This is a sample post.", "userId": 1}
}
next_id = 2  # tracks the next available ID for new posts


# GET /posts/{post_id} - retrieves a single post by its ID
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    if post_id not in posts:
        # HTTPException sends a proper HTTP error response back to the client
        raise HTTPException(status_code=404, detail="Post not found")
    return posts[post_id]


# POST /posts - creates a new post and returns it with a generated ID
@app.post("/posts", status_code=201)
def create_post(post: Post):
    global next_id
    new_post = {"id": next_id, **post.model_dump()}
    posts[next_id] = new_post
    next_id += 1
    return new_post


# PUT /posts/{post_id} - replaces an existing post entirely with new data
@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    posts[post_id] = {"id": post_id, **post.model_dump()}
    return posts[post_id]


# DELETE /posts/{post_id} - removes a post and returns an empty response
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    del posts[post_id]
    return {}
