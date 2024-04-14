from unittest.mock import MagicMock, patch

from app.domain.entities.file import File
from app.infra.database.connection import Connection
from app.infra.database.repositories.file_repository import FileRepository
from tests.helpers.fake_database import FakeDB
from tests.helpers.generate_entities import make_file


def test_should_insert_file():
    with patch.object(Connection, "get_database") as db:
        mocked_db = FakeDB()

        db.return_value = mocked_db

        repository = FileRepository()

        file = make_file()

        mocked_db.commit = MagicMock()
        mocked_db.cursor = MagicMock(return_value=mocked_db)
        mocked_db.execute = MagicMock()

        saved = repository.insert_one(file)

        assert isinstance(saved, File) == True

        mocked_db.commit.assert_called_once()
        mocked_db.cursor.assert_called_once()
        mocked_db.execute.assert_called_once()
