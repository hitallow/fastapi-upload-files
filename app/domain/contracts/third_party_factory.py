from abc import ABC, abstractmethod

from app.domain.contracts.queue import Queue
from app.domain.contracts.storage import Storage


class ThirdPartyFactoryContract(ABC):
    @abstractmethod
    def get_queue(self) -> Queue:
        raise NotImplementedError()

    @abstractmethod
    def get_storage(self) -> Storage:
        raise NotImplementedError()
