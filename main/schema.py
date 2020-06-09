from pydantic import BaseModel
from typing import List, Dict


class User(BaseModel):
    email: str
    preferences: List[str]


class UserSchema(BaseModel):
    status: str
    data: User


class TagsSchema(BaseModel):
    status: str = "ok"
    data: list


class ArticleSchema(BaseModel):
    website_name: str
    title: str
    content: str
    thumbnail: str
    publish_date: str
    tags: List[str]
    url: str
    searched_for: str

    class Config:
        orm_mode = True


class ArticleList(BaseModel):
    status: str
    total_length: int
    data: List[ArticleSchema]
