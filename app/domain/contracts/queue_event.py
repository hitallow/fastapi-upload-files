from abc import ABC, abstractmethod
from ast import Dict
from typing import Any


class QueueEvent(ABC):

    @abstractmethod
    def get_payload(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_event_name(self) -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def from_payload(event: Dict) -> "QueueEvent":
        raise NotImplementedError()

    def get_delay_seconds(self) -> int:
        return 0
