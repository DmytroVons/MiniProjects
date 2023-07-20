import logging

from flask import Flask, Response
from flask import request

from src.tasks import db_setup
from src.services import (
    GetRatesService,
)

logging.basicConfig(level=logging.INFO)

# NOTE: to not overcomplicate task, imagine that it works on schedule (from tasks queue, e.g. RabbitMQ/Amazon SQS, etc)
# from src.tasks import rate_puller
# rate_puller.pull_rates()

db_setup.prepare_db()
app = Flask(__name__)


@app.get('/api/rates')
def get_rates() -> Response:
    service = GetRatesService()
    return service.handle_request(request)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
