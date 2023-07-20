import datetime
import uuid
from dataclasses import dataclass, field, astuple, asdict
from typing import Self

from .settings import get_settings


@dataclass
class Rate:
    baseCurrency: str
    currency: str
    rate: float
    addDate: datetime.datetime = field(default_factory=datetime.datetime.now)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_tuple(self) -> tuple[any, ...]:
        return astuple(self)

    def to_dict(self) -> dict[str, any]:
        # todo: mb make sqlite DB convertor instead ?
        rate = asdict(self)
        timestamp_str = rate['addDate'].strftime(get_settings().TIME_FORMAT)
        rate['addDate'] = timestamp_str
        return rate

    @classmethod
    def from_tuple(cls, t: tuple[str, str, str, float, str]) -> Self:
        id_, base, currency, rate, timestamp = t
        return cls(
            id=id_,
            baseCurrency=base,
            currency=currency,
            rate=rate,
            addDate=datetime.datetime.fromisoformat(timestamp),
        )


@dataclass
class RatesQuery:
    currencyName: str | None
    startDate: str | None
    endDate: str | None

    def to_dict(self) -> dict[str, any]:
        return asdict(self)
