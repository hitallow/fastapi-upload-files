from datetime import datetime
from unittest.mock import ANY, MagicMock, call, patch

import pytest

from app.domain.exceptions.entity_not_found_exception import \
    EntityNotFoundException
from app.infra.database.connection import Connection
from app.infra.database.repositories.file_import_repository import \
    FileImportRepository
from tests.helpers.fake_database import FakeDB
from tests.helpers.generate_entities import make_file_import


def test_should_raise_error_on_get_file_import_by_id(faker):
    mocked_db = FakeDB()
    mocked_db.execute = MagicMock(return_value=mocked_db)
    mocked_db.fetchone = MagicMock(return_value=None)
    file_import_id = faker.uuid4()

    with patch.object(Connection, "get_database", return_value=mocked_db):
        repository = FileImportRepository()

    with pytest.raises(EntityNotFoundException):
        repository.get_by_id(file_import_id)

    mocked_db.execute.assert_called_once_with(
        "SELECT id, title, status, createdAt, updatedAt FROM fileImport  WHERE id = ?",
        (file_import_id,),
    )
    mocked_db.fetchone.assert_called_once()


def test_should_execute_get_by_id_with_success(faker):
    mocked_db = FakeDB()
    file_import_id = faker.uuid4()
    mocked_db.execute = MagicMock(return_value=mocked_db)
    title = faker.word()
    status = faker.word()
    created_at = int(faker.unix_time())
    updated_at = int(faker.unix_time())

    mocked_db.fetchone = MagicMock(
        return_value=[
            file_import_id,
            title,
            status,
            datetime.fromtimestamp(created_at).strftime("%Y-%m-%d %H:%M:%S"),
            datetime.fromtimestamp(updated_at).strftime("%Y-%m-%d %H:%M:%S"),
        ]
    )
    with patch.object(Connection, "get_database", return_value=mocked_db):
        repository = FileImportRepository()

    file_import = repository.get_by_id(file_import_id)

    mocked_db.execute.assert_called_once_with(
        "SELECT id, title, status, createdAt, updatedAt FROM fileImport  WHERE id = ?",
        (file_import_id,),
    )
    mocked_db.fetchone.assert_called_once()

    assert file_import.id == file_import_id
    assert file_import.title == title
    assert file_import.status == status
    assert file_import.created_at == created_at
    assert file_import.updated_at == updated_at


def test_should_update_status(faker):
    mocked_db = FakeDB()

    file_import_id = faker.uuid4()
    status = faker.word()

    mocked_db.execute = MagicMock(return_value=mocked_db)
    mocked_db.commit = MagicMock(return_value=mocked_db)
    mocked_db.fetchone = MagicMock(
        return_value=[
            file_import_id,
            faker.word(),
            status,
            datetime.fromtimestamp(faker.unix_time()).strftime("%Y-%m-%d %H:%M:%S"),
            datetime.fromtimestamp(faker.unix_time()).strftime("%Y-%m-%d %H:%M:%S"),
        ]
    )

    with patch.object(Connection, "get_database", return_value=mocked_db):
        repository = FileImportRepository()

    repository.update_status(file_import_id, status)
    mocked_db.commit.assert_called_with()

    mocked_db.execute.assert_has_calls(
        [
            call(
                "UPDATE fileImport SET status = ?, updatedAt = CURRENT_TIMESTAMP WHERE id = ?",
                (status, file_import_id),
            ),
            call(
                "SELECT id, title, status, createdAt, updatedAt FROM fileImport  WHERE id = ?",
                (file_import_id,),
            ),
        ]
    )


def test_should_insert_one_file_import(faker):
    mocked_db = FakeDB()
    mocked_db.execute = MagicMock(return_value=mocked_db)
    mocked_db.commit = MagicMock(return_value=mocked_db)
    mocked_db.cursor = MagicMock(return_value=mocked_db)

    with patch.object(Connection, "get_database", return_value=mocked_db):
        repository = FileImportRepository()

    file_import = make_file_import()

    repository.insert_one(file_import)

    mocked_db.cursor.assert_called_once()
    mocked_db.commit.assert_called_once()
    mocked_db.execute.assert_called_once_with(
        "INSERT INTO fileImport (id, title, status, fileId) VALUES (?, ?, ?, ?)",
        (
            ANY,
            file_import.title,
            file_import.status,
            file_import.file.id,  # type: ignore
        ),
    )
