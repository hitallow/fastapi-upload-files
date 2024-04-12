from abc import ABC, abstractmethod

from app.domain.contracts.queue_event import QueueEvent


class Handler(ABC):
    @abstractmethod
    def handle(self):
        pass

    @abstractmethod
    def set_event(self, event: QueueEvent):
        pass
