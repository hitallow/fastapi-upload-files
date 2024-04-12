from abc import ABC, abstractmethod


class Logging(ABC):
    @abstractmethod
    def info(self, info) -> None:
        raise NotImplementedError()

    @abstractmethod
    def error(self, error) -> None:
        raise NotImplementedError()

    @abstractmethod
    def debug(self, debug) -> None:
        raise NotImplementedError()
