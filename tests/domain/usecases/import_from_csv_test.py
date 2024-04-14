from unittest.mock import MagicMock, create_autospec

from faker import Faker
from pytest import fixture

from app.domain.contracts.repository_factory import RepositoryFactoryContract
from app.domain.contracts.third_party_factory import ThirdPartyFactoryContract
from app.domain.usecases.handle_import_csv import HandleImportCSVEvent
from app.domain.usecases.import_from_csv import (UploadFromCSVRequest,
                                                 UploadFromCSVUsecase)
from tests.helpers.generate_entities import make_file, make_file_import


@fixture
def sut():
    return UploadFromCSVUsecase(
        repository_factory=create_autospec(RepositoryFactoryContract),
        third_party_factory=create_autospec(ThirdPartyFactoryContract),
    )


def test_should_execute(sut: UploadFromCSVUsecase, faker: Faker):
    file = make_file()
    file_import = make_file_import()

    sut.storage.upload = MagicMock(return_value=file)
    sut.file_import_repository.insert_one = MagicMock(return_value=file_import)
    sut.file_repository.insert_one = MagicMock(return_value=file)
    sut.queue.publish = MagicMock()

    response = sut.execute(
        UploadFromCSVRequest(
            file=faker.word(),
            filename=faker.file_name(),
            size=faker.random_int(100),
        )
    )

    sut.storage.upload.assert_called_once()
    sut.file_import_repository.insert_one.assert_called_once()
    sut.file_repository.insert_one.assert_called_once()
    sut.queue.publish.assert_called_once_with(
        HandleImportCSVEvent(
            file_import_id=file_import.id,  # type: ignore
            filename=file.filename,
            target=0,
            lines=500,
        )
    )
