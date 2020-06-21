from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os

app = FastAPI(
    title="blogie", openapi_url="/api/openapi.json", docs_url=None, redoc_url="/api/doc"
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
