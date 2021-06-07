from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv

import os


load_dotenv()  # take environment variables from .env.


app = FastAPI(
    title="Blogie-API",
    description="A super simple REST API which allows you \
    to search articles from a vast majority of websites.\
    \n ### Features:\
    \n - Search for articles with specific tags, e.g. 'bitcoin'.\
    \n - Search for articles using multiple keywords, e.g. 'bitcoin', 'iphone'.\
    \n - Get global news headlines with news source. \
    \n - Free and opensource.\
    \n ### Prerequisites:\
    \n **API key**: You would need a API key for requesting any data \
    from our API. You can generate one by registering \
    an account on blogie and after that do a GET request to '''/api/createtoken/{email}''' \
    with your registered email. \
    ",
    openapi_url="/api/openapi.json",
    docs_url="/swagger",
    redoc_url="/",
)

# set up cross site origin policies
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

SECRET_KEY = os.environ["SECRET_KEY"]

db = client.blogie

from .routes import *
