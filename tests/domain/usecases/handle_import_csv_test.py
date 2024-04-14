import csv
from io import StringIO
from unittest.mock import MagicMock, create_autospec

from pytest import fixture

from app.domain.contracts.repository_factory import RepositoryFactoryContract
from app.domain.contracts.third_party_factory import ThirdPartyFactoryContract
from app.domain.exceptions.file_not_found_exception import \
    FileNotFoundException
from app.domain.exceptions.publish_queue_task_exception import \
    PublishQueueTaskException
from app.domain.usecases.handle_import_csv import (HandleImportCSVEvent,
                                                   HandleImportCSVUsecase)


@fixture
def sut():
    return HandleImportCSVUsecase(
        repository_factory=create_autospec(RepositoryFactoryContract),
        third_party_factory=create_autospec(ThirdPartyFactoryContract),
    )


@fixture
def event(faker):
    return HandleImportCSVEvent.from_payload(
        {
            "fileImportId": f"{faker.uuid4()}.csv",
            "filename": faker.file_name(),
            "target": faker.random_int(min=0),
            "lines": 1000,
        }
    )


def mount_fake_csv(faker, qtd_rows: int):
    file = StringIO()
    csv_d = csv.writer(file, delimiter=",")

    csv_d.writerow(
        ["name", "debtAmount", "email", "governmentId", "debtId", "debtDueDate"],
    )

    for _ in range(qtd_rows):
        csv_d.writerow(
            [
                faker.first_name(),
                faker.random_int(min=10),
                faker.email(),
                faker.bothify("########"),
                faker.bothify("########"),
                faker.date(),
            ]
        )

    file.seek(0)

    return file.getvalue().encode()


def test_should_assert_event_name(event: HandleImportCSVEvent):
    assert event.get_event_name() == "importBoletosFromCSV"


def test_should_assert_payload_data(event: HandleImportCSVEvent):
    assert event.get_payload() == {
        "fileImportId": event.file_import_id,
        "filename": event.filename,
        "target": event.target,
        "lines": event.lines,
    }


def test_should_get_error_on_file(
    sut: HandleImportCSVUsecase, event: HandleImportCSVEvent
):
    sut.set_event(event)

    sut.storage.load = MagicMock(side_effect=FileNotFoundException)

    sut.file_import_repository.update_status = MagicMock()

    sut.handle()

    sut.storage.load.assert_called_once_with(event.filename)
    sut.file_import_repository.update_status.assert_called_once_with(
        event.file_import_id, "error"
    )


def test_should_catch_generic_exception(
    sut: HandleImportCSVUsecase, event: HandleImportCSVEvent
):
    sut.set_event(event)

    sut.storage.load = MagicMock(side_effect=Exception)

    sut.file_import_repository.update_status = MagicMock()

    sut.handle()

    sut.storage.load.assert_called_once_with(event.filename)
    sut.file_import_repository.update_status.assert_called_once_with(
        event.file_import_id, "error"
    )


def test_not_found_rows_in_slice(
    sut: HandleImportCSVUsecase, event: HandleImportCSVEvent
):
    sut.set_event(event)

    sut.storage.load = MagicMock(return_value=b"")

    sut.file_import_repository.update_status = MagicMock()

    sut.handle()

    sut.storage.load.assert_called_once_with(event.filename)
    sut.file_import_repository.update_status.assert_called_once_with(
        event.file_import_id, "done"
    )


def test_should_get_publish_error(
    sut: HandleImportCSVUsecase, event: HandleImportCSVEvent, faker
):

    total_items = faker.random_int(min=50, max=100)
    event.target = total_items - 50
    sut.set_event(event)

    sut.storage.load = MagicMock(return_value=mount_fake_csv(faker, total_items))
    sut.queue.publish = MagicMock(side_effect=PublishQueueTaskException())

    sut.file_import_repository.update_status = MagicMock()

    sut.handle()

    sut.queue.publish.assert_called_once()

    sut.storage.load.assert_called_once_with(event.filename)
    sut.file_import_repository.update_status.assert_called_once_with(
        event.file_import_id, "error"
    )


def test_storage_entities_and_in_queue(
    sut: HandleImportCSVUsecase, event: HandleImportCSVEvent, faker
):

    total_items = faker.random_int(min=50, max=100)
    event.target = total_items - 50
    sut.set_event(event)

    sut.storage.load = MagicMock(return_value=mount_fake_csv(faker, total_items))
    sut.queue.publish = MagicMock()

    sut.file_import_repository.update_status = MagicMock()

    sut.handle()

    sut.queue.publish.assert_called_once()

    sut.storage.load.assert_called_once_with(event.filename)
    sut.file_import_repository.update_status.assert_not_called()
