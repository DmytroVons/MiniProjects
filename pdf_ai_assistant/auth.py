from os import getenv

from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from http import HTTPStatus

api_key_header = APIKeyHeader(name="access_token", auto_error=False)


def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == getenv("API_KEY"):
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Could not validate API KEY"
        )
