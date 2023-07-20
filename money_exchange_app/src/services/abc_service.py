from abc import ABC
from abc import abstractmethod

from flask import Request, Response


class ABCService(ABC):

    @abstractmethod
    def handle_request(self, request: Request) -> Response:
        raise NotImplementedError()
