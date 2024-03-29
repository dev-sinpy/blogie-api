import xml.etree.ElementTree as ET

from main import db

import requests


class User:
    def __init__(self, email: str, tags: list = None):
        self.email = email
        if tags is None:
            self.tags = []
        else:
            self.tags = tags

    def get_user(self):
        collection = db["user"]
        user = collection.find_one({"email": self.email})
        if not user:
            raise Exception
        return user

    def set_user(self):
        collection = db["user"]
        user = collection.find_one({"email": self.email})
        if user:
            raise Exception
        collection.insert_one({"email": self.email, "preferences": []})
        return True

    def update_user(self):
        collection = db["user"]
        collection.update_one(
            {"email": self.email},
            {"$set": {"email": self.email, "preferences": self.tags}},
        )
        return True

    def delete_user(self):
        collection = db["user"]
        collection.delete_one({"email": self.email})

        return True


def get_tags():
    collection = db["tags"]
    tags = collection.find_one({})
    return tags["tags"]


def get_article_by_tag(tag, limit, page):
    collection = db["data"]
    skip = limit if page > 1 else 0
    articles = []
    for article in collection.find({"tags": tag}, skip=skip, limit=limit).sort(
        "publish_date", -1
    ):
        article["searched_for"] = tag
        articles.append(article)
    return articles


def get_articles(tags, limit, page):
    articles = []
    bisect = limit // len(tags)
    for tag in tags:
        articles.extend(get_article_by_tag(tag, bisect, page))
    return articles

def get_news() -> list:
    rss = requests.get("https://news.google.com/rss/search?q=news").content
    root = ET.fromstring(rss)[0]
    articles = []
    for item in root.findall("item"):
        article = {"title": item.find("title").text, "source": item.find("link").text}
        articles.append(article)

    return articles
