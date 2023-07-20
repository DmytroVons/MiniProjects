import logging
import datetime

from src.dtos import Rate
from src.settings import get_settings
from src.rate_repository import RateRepository
from src.clients import CurrencyClient, InvalidAPIResponse

logger = logging.getLogger(__name__)


def pull_rates() -> None:
    settings = get_settings()
    pull_time = datetime.datetime.now()

    logger.info(f'Pulling rates... Current time: {pull_time.strftime(settings.TIME_FORMAT)}')
    try:
        response = CurrencyClient(settings).get_rates()
    except AssertionError as e:
        logger.error(e)
        raise InvalidAPIResponse(str(e))

    rates = response['rates']
    rates_to_add = []
    for currency in settings.CURRENCIES_TO_FIND:
        try:
            rate = rates[currency]
        except KeyError as e:
            msg = f'{e} currency not found.'
            logging.error(msg)
            raise InvalidAPIResponse(msg) from e

        # NOTE: use Decimal module for wokring with such rate. float is here bc I'm lazy
        rates_to_add.append(Rate(
            baseCurrency=settings.BASE_CURRENCY,
            currency=currency,
            rate=float(f'{rate:.4f}'),
            addDate=pull_time,
        ))

    rate_repository = RateRepository()
    rate_repository.add_rates_batch(rates_to_add)
