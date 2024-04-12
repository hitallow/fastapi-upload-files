from abc import ABC, abstractmethod
from typing import Any


class QueueEvent(ABC):

    @abstractmethod
    def get_payload(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_event_name(self) -> str:
        raise NotImplementedError

    def get_delay_seconds(self) -> int:
        return 0
