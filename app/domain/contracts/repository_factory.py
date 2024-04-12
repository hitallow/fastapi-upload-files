from abc import ABC, abstractmethod

from app.domain.contracts.boleto_repository import BoletoRepositoryContract
from app.domain.contracts.file_import_repository import \
    FileImportRepositoryContract
from app.domain.contracts.file_repository import FileRepositoryContract


class RepositoryFactoryContract(ABC):
    @abstractmethod
    def get_file_import_repository(self) -> FileImportRepositoryContract:
        raise NotImplementedError()

    @abstractmethod
    def get_file_repository(self) -> FileRepositoryContract:
        raise NotImplementedError()

    @abstractmethod
    def get_boleto_repository(self) -> BoletoRepositoryContract:
        raise NotImplementedError()
