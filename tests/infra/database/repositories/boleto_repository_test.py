from unittest.mock import ANY, MagicMock, call, patch

import pytest

from app.domain.exceptions.entity_not_found_exception import \
    EntityNotFoundException
from app.infra.database.connection import Connection
from app.infra.database.repositories.boleto_repository import BoletoRepository
from tests.helpers.fake_database import FakeDB
from tests.helpers.generate_entities import make_boleto


def test_should_raise_exception_on_get_boleto_by_id(faker, fake_database: FakeDB):

    with patch.object(Connection, "get_database", return_value=fake_database):
        repository = BoletoRepository()

    fake_database.execute = MagicMock(return_value=fake_database)
    fake_database.fetchone = MagicMock(return_value=None)

    boleto_id = faker.uuid4()
    with pytest.raises(EntityNotFoundException):
        repository.get_by_id(boleto_id)

    fake_database.fetchone.assert_called_once()
    fake_database.execute.assert_called_once_with(
        f"select id, name, debitId, governmentId, email, debitAmount, dueDate from boleto WHERE id = '{boleto_id}';"
    )


def test_should_load_a_boleto_by_id(faker, fake_database: FakeDB):

    with patch.object(Connection, "get_database", return_value=fake_database):
        repository = BoletoRepository()

    fake_database.execute = MagicMock(return_value=fake_database)

    boleto_id = faker.uuid4()
    name = faker.first_name()
    debit_id = faker.bothify("########")
    government_id = faker.bothify("########")
    email = faker.email()
    debit_amount = faker.random_int(10)
    due_date = int(faker.unix_time())

    fake_database.fetchone = MagicMock(
        return_value=[
            boleto_id,
            name,
            debit_id,
            government_id,
            email,
            debit_amount,
            due_date,
        ]
    )

    boleto = repository.get_by_id(boleto_id)

    fake_database.fetchone.assert_called_once()
    fake_database.execute.assert_called_once_with(
        f"select id, name, debitId, governmentId, email, debitAmount, dueDate from boleto WHERE id = '{boleto_id}';"
    )

    assert boleto.id == boleto_id
    assert boleto.name == name
    assert boleto.debit_id == debit_id
    assert boleto.government_id == government_id
    assert boleto.email == email
    assert boleto.debit_amount == debit_amount
    assert boleto.due_date == due_date


def test_should_insert_one_boleto(fake_database: FakeDB):

    fake_database.commit = MagicMock()
    fake_database.execute = MagicMock()
    fake_database.cursor = MagicMock(return_value=fake_database)

    boleto = make_boleto()
    boleto.id = None

    with patch.object(
        Connection, "get_database", return_value=fake_database
    ), patch.object(Connection, "get_new_connection", return_value=fake_database):
        repository = BoletoRepository()
        saved = repository.insert_one(boleto)

    assert saved.id is not None

    fake_database.commit.assert_called_once()
    fake_database.cursor.assert_called_once()
    fake_database.execute.assert_called_once_with(
        "INSERT INTO boleto (id, name, debitId, governmentId, email, debitAmount, dueDate) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            saved.id,
            boleto.name,
            boleto.debit_id,
            boleto.government_id,
            boleto.email,
            boleto.debit_amount,
            boleto.due_date,
        ),
    )


def test_should_insert_many_boleto(faker, fake_database: FakeDB):

    fake_database.commit = MagicMock()
    fake_database.executemany = MagicMock()

    total_items = faker.random_int(min=1, max=99)

    boletos = [make_boleto() for _ in range(total_items)]

    with patch.object(
        Connection, "get_database", return_value=fake_database
    ), patch.object(Connection, "get_new_connection", return_value=fake_database):
        repository = BoletoRepository()
        saved = repository.insert_many(boletos)

    for item in saved:
        assert item.id is not None

    fake_database.commit.assert_called_once()
    fake_database.executemany.assert_called_once_with(
        "INSERT INTO boleto (id, name, debitId, governmentId, email, debitAmount, dueDate) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            (
                ANY,
                boleto.name,
                boleto.debit_id,
                boleto.government_id,
                boleto.email,
                boleto.debit_amount,
                boleto.due_date,
            )
            for boleto in boletos
        ],
    )


@pytest.mark.parametrize(
    ["limit", "offset", "from_date"],
    [
        (None, None, None),
        (10, 10, None),
        (None, None, 1),
        (10, 10, 0),
    ],
)
def test_should_test_all_cases_of_get_all(
    limit: int,
    offset: int,
    from_date: int,
    faker,
    fake_database: FakeDB,
):
    total_items = faker.random_int(min=1, max=100)

    boletos = [make_boleto() for _ in range(total_items)]

    fake_database.execute = MagicMock(return_value=fake_database)
    fake_database.fetchall = MagicMock(
        return_value=[
            (
                b.id,
                b.name,
                b.debit_id,
                b.government_id,
                b.email,
                b.debit_amount,
                b.due_date,
            )
            for b in boletos
        ]
    )
    fake_database.fetchone = MagicMock(return_value=[total_items])

    with patch.object(Connection, "get_database", return_value=fake_database):
        repository = BoletoRepository()

    paginated = repository.get_all(limit=limit, offset=offset, from_date=from_date)

    assert paginated.total_items == total_items
    assert len(paginated.items) == len(boletos)
    fake_database.fetchone.assert_called_once()
    fake_database.fetchall.assert_called_once()

    sql_of_query = "select id, name, debitId, governmentId, email, debitAmount, dueDate from boleto"

    if limit is not None and offset is not None and from_date is not None:
        sql_of_query = f"select id, name, debitId, governmentId, email, debitAmount, dueDate from boleto WHERE dueDate = {from_date} LIMIT {limit} OFFSET {offset * limit}"
    elif limit is not None and offset is not None:
        sql_of_query = f"select id, name, debitId, governmentId, email, debitAmount, dueDate from boleto LIMIT {limit} OFFSET {offset * limit}"
    elif from_date is not None:
        sql_of_query = f"select id, name, debitId, governmentId, email, debitAmount, dueDate from boleto WHERE dueDate = {from_date}"

    fake_database.execute.assert_has_calls(
        [
            call(sql_of_query),
            call("select count(*) as total from boleto;"),
        ]
    )
