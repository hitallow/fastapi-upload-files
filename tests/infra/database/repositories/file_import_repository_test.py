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


@pytest.mark.parametrize(
    ["limit", "offset"],
    [
        (10, None),
        (None, None),
        (None, 10),
        (10, 10),
    ],
)
def test_should_test_all_cases_of_get_all(
    limit: int,
    offset: int,
    faker,
    fake_database: FakeDB,
):
    total_items = faker.random_int(min=1, max=100)

    files_import = [make_file_import() for _ in range(total_items)]

    fake_database.execute = MagicMock(return_value=fake_database)
    fake_database.fetchall = MagicMock(
        return_value=[
            (
                f.id,
                f.title,
                f.status,
                datetime.fromtimestamp(f.created_at).strftime("%Y-%m-%d %H:%M:%S"),
                datetime.fromtimestamp(f.updated_at).strftime("%Y-%m-%d %H:%M:%S"),
            )
            for f in files_import
        ]
    )
    fake_database.fetchone = MagicMock(return_value=[total_items])

    with patch.object(Connection, "get_database", return_value=fake_database):
        repository = FileImportRepository()

    paginated = repository.get_all(limit=limit, offset=offset)

    assert paginated.total_items == total_items
    assert len(paginated.items) == len(files_import)
    fake_database.fetchone.assert_called_once()
    fake_database.fetchall.assert_called_once()

    sql_of_query = "SELECT id, title, status, createdAt, updatedAt FROM fileImport"

    if limit is not None and offset is not None:
        sql_of_query = f"SELECT id, title, status, createdAt, updatedAt FROM fileImport LIMIT {limit} OFFSET {offset * limit}"

    fake_database.execute.assert_has_calls(
        [
            call(sql_of_query),
            call("select count(*) as total from fileImport;"),
        ]
    )
