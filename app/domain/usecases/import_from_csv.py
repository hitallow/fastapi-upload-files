from time import time
from typing import Any
from uuid import uuid4

from app.domain.contracts.repository_factory import RepositoryFactoryContract
from app.domain.contracts.third_party_factory import ThirdPartyFactoryContract
from app.domain.contracts.usecase import Usecase
from app.domain.entities import File, FileImport
from app.domain.entities.entity import Entity
from app.domain.usecases.handle_import_csv import HandleImportCSVEvent


class UploadFromCSVRequest(Entity):
    file: Any
    filename: str
    size: int


class UploadFromCSVResponse(Entity):
    file_import: FileImport


class UploadFromCSVUsecase(Usecase[UploadFromCSVRequest, UploadFromCSVResponse]):
    def __init__(
        self,
        repository_factory: RepositoryFactoryContract,
        third_party_factory: ThirdPartyFactoryContract,
    ) -> None:
        self.file_import_repository = repository_factory.get_file_import_repository()
        self.file_repository = repository_factory.get_file_repository()
        self.storage = third_party_factory.get_storage()
        self.queue = third_party_factory.get_queue()
        self.logging = third_party_factory.get_logging()

    def execute(self, file: UploadFromCSVRequest) -> UploadFromCSVResponse:
        imported_file = self.storage.upload(
            File(
                filename=f"{str(uuid4())}.csv",
                orignalFilename=file.filename,
                size=file.size,
                tempFile=file.file,
            )
        )

        file_import = self.file_import_repository.insert_one(
            FileImport(
                title="UploadCSV",
                status="processing",
                created_at=int(time()),
                updated_at=int(time()),
                file=self.file_repository.insert_one(imported_file),
            )
        )

        self.logging.info("arquivo salvo, iniciando importação ...")

        # self.queue.publish(
        #     HandleImportCSVEvent(
        #         file_import_id=file_import.id,  # type: ignore
        #         filename=imported_file.filename,
        #         target=0,
        #         lines=500,
        #     )
        # )

        return UploadFromCSVResponse(
            file_import=file_import
        )
