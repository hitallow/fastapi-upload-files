from io import StringIO
from unittest.mock import MagicMock, patch

from app.infra.database.connection import Connection
from app.infra.database.migration_runner.migration_runner import \
    MigrationRunner
from tests.helpers.fake_database import FakeDB


def test_should_not_found_files(fake_database: FakeDB, faker):

    fake_database.executescript = MagicMock()

    fake_database.execute = MagicMock(return_value=fake_database)
    fake_database.fetchone = MagicMock(return_value=False)
    fake_database.close = MagicMock()
    fake_database.commit = MagicMock()

    class FakeOpenWrapper:
        def __init__(self, *params) -> None:
            pass

        def __enter__(self, *params):

            s = StringIO(faker.word())
            s.seek(0)
            return s

        def __exit__(self, *params):
            return

    total_files = faker.random_int(min=1, max=100)
    files = [f"{faker.unix_time()}.sql" for _ in range(total_files)]

    with (
        patch.object(Connection, "get_database", return_value=fake_database),
        patch(
            "os.listdir",
            return_value=files,
        ) as listdir,
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", FakeOpenWrapper),
    ):
        sut = MigrationRunner()
        sut.execute()

    assert fake_database.executescript.call_count == total_files
    assert fake_database.execute.call_count == total_files * 2
    assert fake_database.fetchone.call_count == total_files
    assert fake_database.commit.call_count == total_files
    listdir.assert_called_once()
    fake_database.close.assert_called_once()
