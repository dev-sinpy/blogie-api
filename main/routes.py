from typing import List
from main import app
from .schema import UserSchema, ArticleSchema, ArticleList, NewsList, TagsSchema
from main.db_queries import *
from fastapi import Depends, HTTPException, Query
from random import shuffle


async def main_params(q: str, limit: int = 20, page: int = 1):
    limit: int = Query(20, title="hfehf", min_length=10, max_length="50")
    return {"q": q.split(","), "limit": limit, "page": page}


async def user_params(email: str, tags: str):
    return {"email": email, "tags": tags.split(",")}


@app.get("/api/", response_model=ArticleList)
async def search(
    q: str = Query(
        ...,
        title="query string",
        description="Topics you want to search for. If you want to search for multiple tags then separate them with a comma.",
    ),
    limit: int = Query(20, title="limit", description="Limit response", ge=10, le=80,),
    page: int = Query(
        1, title="page", description="To skip over next page of response.", ge=1, le=10
    ),
):
    """
    Endpoint for searching articles.
    """
    tags: list = q.split(",")
    shuffle(tags)
    articles: list = get_articles(tags, limit, page)
    return {"status": "ok", "total_length": len(articles), "data": articles}


@app.get("/api/news/", response_model=NewsList)
async def news():
    """
    Returns global news headlines.
    """
    news = get_news()
    return {"status": "ok", "total_length": len(news), "data": news}


@app.get("/api/tags/", include_in_schema=False, response_model=TagsSchema)
async def tags():
    return {"status": "ok", "data": get_tags()}


@app.get("/api/user/{email}", include_in_schema=False, response_model=UserSchema)
async def user(email: str):
    try:
        user = User(email)
        response = {"status": "ok", "data": user.get_user()}
        return response

    except Exception:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/api/setuser/{email}", include_in_schema=False, status_code=201)
async def set_user(email: str):
    try:
        user = User(email)
        user.set_user()
        return {"status": "ok"}

    except Exception as err:
        raise HTTPException(status_code=406, detail="email already in use")


@app.post("/api/updateuser/", include_in_schema=False, status_code=200)
async def update_user(params: dict = Depends(user_params)):
    email = params["email"]
    tags = params["tags"]
    user = User(email, tags)
    user.update_user()

    return {"status": "ok"}


@app.post("/api/deleteuser/{email}", include_in_schema=False, status_code=200)
async def delete_user(email: str):
    user = User(email)
    user.delete_user()

    return {"status": "ok"}
