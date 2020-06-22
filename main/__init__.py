from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os

app = FastAPI(
    title="Blogie-API",
    description="A super simple REST API which allows you to search articles from a vast majority of websites.",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/doc",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_event_handler("startup", start_db_connection)
# app.add_event_handler("shutdown", close_db_connection)

client = MongoClient(os.environ["DB_URI"])

db = client.blogie

from .routes import *
