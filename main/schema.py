from datetime import date
from typing import List, Dict, Optional

from pydantic import BaseModel


class TagsSchema(BaseModel):
    status: str = "ok"
    data: list


class ArticleSchema(BaseModel):
    website_name: str
    title: str
    content: str
    thumbnail: str
    publish_date: date
    tags: List[str]
    url: str
    searched_for: str

    class Config:
        orm_mode = True


class ArticleList(BaseModel):
    status: str
    total_length: int
    data: List[ArticleSchema]


class NewsSchema(BaseModel):
    title: str
    source: str


class NewsList(BaseModel):
    status: str
    total_length: int
    data: List[NewsSchema]


class Token(BaseModel):
    status: str
    access_token: str
