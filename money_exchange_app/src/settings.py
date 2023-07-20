import os
from pathlib import Path
from functools import cache
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv(Path().parent.absolute())

DEFAULT_CURRENCIES_TO_FIND = ['USD']


@dataclass(frozen=True)
class Settings:
    DB_CONNECTION_URL: str
    CURRENCY_API_KEY: str
    CURRENCY_API_GET_RATES_URL: str
    CURRENCIES_TO_FIND: list[str]
    BASE_CURRENCY: str = 'USD'
    TIME_FORMAT: str = '%Y-%m-%dT%H:%M:%SZ'
    GET_RATES_QUERY_TIME_FORMAT: str = '%Y-%m-%d'


@cache
def get_settings() -> Settings:
    currencies_to_find = os.environ.get('CURRENCY_TO_FIND')
    currencies_to_find = currencies_to_find.split(',') if currencies_to_find else DEFAULT_CURRENCIES_TO_FIND

    return Settings(
        DB_CONNECTION_URL=os.environ['DB_CONNECTION_URL'],
        CURRENCY_API_KEY=os.environ['CURRENCY_API_KEY'],
        CURRENCY_API_GET_RATES_URL=os.environ['CURRENCY_API_GET_RATES_URL'],
        CURRENCIES_TO_FIND=currencies_to_find,
    )
