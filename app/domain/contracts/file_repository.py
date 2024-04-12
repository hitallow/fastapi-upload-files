from abc import ABC, abstractmethod

from app.domain.entities.file import File


class FileRepositoryContract(ABC):
    @abstractmethod
    def insert_one(self, file: File) -> File:
        raise NotImplementedError
