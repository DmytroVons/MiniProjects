import logging
from http import HTTPStatus
from typing import Self

import requests

from src.settings import Settings

logger = logging.getLogger(__name__)


class InvalidAPIResponse(ValueError):
    pass


class CurrencyClient:
    _instance: Self = None

    def __new__(cls, *args, **kwargs) -> 'CurrencyClient':
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, settings: Settings) -> None:
        self._base_currency = settings.BASE_CURRENCY
        self._get_rates_url = settings.CURRENCY_API_GET_RATES_URL
        self._api_key = settings.CURRENCY_API_KEY

    def get_rates(self) -> dict[str, any]:
        # https://currencyapi.net/documentation

        params = {
            'key': self._api_key,
            'base': self._base_currency,
            'output': 'JSON',
        }

        response = requests.get(self._get_rates_url, params=params)
        try:
            assert response.status_code == HTTPStatus.OK, \
                f'Invalid API response: {response.status_code}, {response.text}'
        except AssertionError as e:
            logger.error(e)
            raise InvalidAPIResponse(str(e)) from e

        try:
            return response.json()
        except ValueError as e:
            msg = f'Failed to parse API response. Response: {response.text}. Error: {e}'
            logger.error(msg)
            raise InvalidAPIResponse(msg) from e
