from typing import List
from main import app
from .schema import UserSchema, ArticleSchema, ArticleList, TagsSchema
from main.db_queries import *
from fastapi import Depends, HTTPException


async def main_params(q: str, limit: int = 20, page: int = 1):
    return {"q": q.split(","), "limit": limit, "page": page}


async def user_params(email: str, tags: str):
    return {"email": email, "tags": tags.split(",")}


@app.get("/api/", response_model=ArticleList)
async def user(params: dict = Depends(main_params)):
    tags = params["q"]
    limit = params["limit"]
    page = params["page"]
    articles = get_articles(tags, limit, page)
    return {"status": "ok", "total_length": len(articles), "data": articles}


@app.get("/api/tags/", response_model=TagsSchema)
async def user():
    return {"status": "ok", "data": get_tags()}


@app.get("/api/user/{email}", response_model=UserSchema)
async def user(email: str):
    try:
        user = User(email)
        response = {"status": "ok", "data": user.get_user()}
        return response

    except Exception:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/api/setuser/{email}", status_code=201)
async def user(email: str):
    try:
        user = User(email)
        user.set_user()
        return {"status": "ok"}

    except Exception as err:
        raise HTTPException(status_code=406, detail="email already in use")


@app.post("/api/updateuser/", status_code=200)
async def user(params: dict = Depends(user_params)):
    email = params["email"]
    tags = params["tags"]
    user = User(email, tags)
    user.update_user()

    return {"status": "ok"}


@app.post("/api/deleteuser/{email}", status_code=200)
async def user(email: str):
    user = User(email)
    user.delete_user()

    return {"status": "ok"}
