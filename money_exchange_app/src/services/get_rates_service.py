import logging
from typing import Self

from flask import Request, Response
from flask import jsonify

from .abc_service import ABCService
from src.dtos import RatesQuery
from src.rate_repository import RateRepository

logger = logging.getLogger(__name__)


class GetRatesService(ABCService):
    _instance: Self = None

    def __new__(cls, *args, **kwargs) -> 'GetRatesService':
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._rate_repository = RateRepository()

    def handle_request(self, request: Request) -> Response:
        query = self._get_query(request)
        if not any(list(query.__dict__.values())):
            return self._get_all_rates()

        return self._get_rates_by_query(query)

    def _get_all_rates(self) -> Response:
        rates = self._rate_repository.get_all_rates()
        rates = [r.to_dict() for r in rates]
        response = {
            'total': len(rates),
            'rates': rates,
        }
        return jsonify(response)

    def _get_rates_by_query(self, query: RatesQuery) -> Response:
        rates = self._rate_repository.get_rates_by_query(query)
        rates = [r.to_dict() for r in rates]
        response = {
            'total': len(rates),
            'currencyName': query.currencyName,
            'startDate': query.startDate,
            'endDate': query.endDate,
            'rates': rates,
        }
        return jsonify(response)

    @staticmethod
    def _get_query(request: Request) -> RatesQuery:
        return RatesQuery(
            currencyName=request.values.get('currencyName'),
            startDate=request.values.get('startDate'),
            endDate=request.values.get('endDate'),
        )
