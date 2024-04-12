from app.domain.contracts.boleto_repository import BoletoRepositoryContract
from app.domain.contracts.file_import_repository import \
    FileImportRepositoryContract
from app.domain.contracts.file_repository import FileRepositoryContract
from app.domain.contracts.repository_factory import RepositoryFactoryContract
from app.infra.database.repositories.boleto_repository import BoletoRepository
from app.infra.database.repositories.file_import_repository import \
    FileImportRepository
from app.infra.database.repositories.file_repository import FileRepository


class RepositoryFactory(RepositoryFactoryContract):

    def get_boleto_repository(self) -> BoletoRepositoryContract:
        return BoletoRepository()

    def get_file_import_repository(self) -> FileImportRepositoryContract:
        return FileImportRepository()

    def get_file_repository(self) -> FileRepositoryContract:
        return FileRepository()
