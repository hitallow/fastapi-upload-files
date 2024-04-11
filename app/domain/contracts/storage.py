from abc import ABC, abstractmethod

from app.domain.entities.file import File


class Storage(ABC):

    @abstractmethod
    def upload(self, file: File) -> File:
        raise NotImplementedError
