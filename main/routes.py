from typing import List
from random import shuffle
from datetime import datetime

from main import app
from .db_queries import User, get_news, get_articles
from .schema import *
from .utils import *

from fastapi import Security, Depends, HTTPException, status, Query
from fastapi.security.api_key import APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import JSONResponse


@app.get("/api/createtoken/{email}", response_model=Token)
async def create_api_key(email: str):
    """
    Endpoint for generating API key for authentication. Make sure to\
     first register an account on blogie and then provide your registered email \
     as a path parameter.
    """
    try:
        user = User(email)
        payload = {"email": email, "iat": datetime.utcnow()}
        access_token = create_access_token(payload)

        return {"status": "ok", "access_token": access_token}

    except Exception as Err:
        print(Err)
        raise HTTPException(status_code=403, detail="User not found")


@app.get("/api/search", response_model=ArticleList)
async def search(
    keywords: str = Query(
        ...,
        title="query string",
        description="Topics you want to search for. If you want to search for multiple tags then separate them with a comma.",
    ),
    limit: int = Query(20, title="limit", description="Limit response", ge=10, le=80,),
    page: int = Query(
        1, title="page", description="To skip over next page of response.", ge=1, le=10
    ),
    api_key: APIKey = Depends(get_api_key),
):
    """
    Endpoint for searching articles.
    """
    tags: list = keywords.split(",")
    shuffle(tags)
    articles: list = get_articles(tags, limit, page)
    return {"status": "ok", "total_length": len(articles), "data": articles}


@app.get("/api/news/", response_model=NewsList)
async def news(api_key: APIKey = Depends(get_api_key)):
    """
    Endpoint for getting global news headlines. This endpoint is currently \
    very limited, but it is still great if you just want to get news headlines from\
    around the world.
    """
    news = get_news()
    return {"status": "ok", "total_length": len(news), "data": news}
