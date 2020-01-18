from abc import ABC
from abc import abstractmethod


class Website(ABC):

    @abstractmethod
    def create_offers(self):
        pass
