from abc import ABC, abstractmethod

from app.domain.contracts.queue_event import QueueEvent


class Queue(ABC):
    @abstractmethod
    def publish(self, event: QueueEvent):
        raise NotImplementedError

    @abstractmethod
    def consume(self):
        raise NotImplementedError
