import datetime

from .dtos import Rate, RatesQuery
from .clients import DBClient
from .settings import get_settings


class RateRepository:
    __slots__ = ('_db_client', '_time_format', '_from_str_time_format')

    def __init__(self) -> None:
        settings = get_settings()

        self._db_client = DBClient(settings.DB_CONNECTION_URL)
        self._time_format = settings.TIME_FORMAT
        self._from_str_time_format = settings.GET_RATES_QUERY_TIME_FORMAT

    def get_all_rates(self) -> list[Rate]:
        statement = 'SELECT * from rates'
        rows = self._db_client.execute(statement)
        return [Rate.from_tuple(row) for row in rows]

    def get_rates_by_query(self, query: RatesQuery) -> list[Rate]:
        where = self._build_where(query)
        statement = 'SELECT * from rates' + ' ' + where
        rows = self._db_client.execute(statement)
        return [Rate.from_tuple(row) for row in rows]

    def add_rates_batch(self, rates: list[Rate]) -> None:
        statement = 'INSERT INTO rates (baseCurrency, currency, rate, addDate, id) VALUES(?, ?, ?, ?, ?)'
        self._db_client.executemany(statement, [r.to_tuple() for r in rates])

    def _build_where(self, query: RatesQuery) -> str:
        ands = []
        if query.currencyName:
            ands.append(f"currency = '{query.currencyName.split()[0].strip()}'")
        if query.startDate:
            start_date = query.startDate.split()[0].strip()
            statement = self._build_date_query(start_date, '>=')
            ands.append(statement)
        if query.endDate:
            end_date = query.endDate.split()[0].strip()
            statement = self._build_date_query(end_date, '<=')
            ands.append(statement)

        where = 'WHERE ' + ' AND '.join(ands)
        return where

    def _build_date_query(self, date_str: str, action: str) -> str:
        date = datetime.datetime.strptime(date_str, self._from_str_time_format)
        return f"addDate {action} datetime('{date.strftime(self._time_format)}')"
