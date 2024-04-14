from abc import ABC, abstractmethod

from app.domain.entities.file_import import FileImport
from app.domain.entities.paginted_list import PaginatedEntities


class FileImportRepositoryContract(ABC):

    @abstractmethod
    def insert_one(self, file_import: FileImport) -> FileImport:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: str) -> FileImport:
        raise NotImplementedError

    @abstractmethod
    def update_status(self, id: str, status: str) -> FileImport:
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> PaginatedEntities[FileImport]:
        raise NotImplementedError
