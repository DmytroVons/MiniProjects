from os import getenv

from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

api_key_header = APIKeyHeader(name="access_token", auto_error=False)


def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == getenv("API_KEY"):
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )
