from .schema import *
from . import SECRET_KEY


from jwt.exceptions import InvalidSignatureError, DecodeError
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from fastapi.security.api_key import APIKeyQuery, APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN

import jwt
import os


API_KEY_NAME = "apikey"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_access_token(access_token: str):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except (InvalidSignatureError, DecodeError):
        return False


async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
):
    access_token = api_key_query if api_key_query else api_key_header
    if decode_access_token(access_token):
        return api_key_query
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
