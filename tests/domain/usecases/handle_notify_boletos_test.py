from unittest.mock import MagicMock, create_autospec

from pytest import fixture

from app.domain.contracts.repository_factory import RepositoryFactoryContract
from app.domain.contracts.third_party_factory import ThirdPartyFactoryContract
from app.domain.entities.paginted_list import PaginatedEntities
from app.domain.usecases.handle_notify_boletos import (
    HandleNotifyBoletosEvent, HandleNotifyBoletosUsecase)
from tests.helpers.generate_entities import make_boleto


@fixture
def sut():
    return HandleNotifyBoletosUsecase(
        repository_factory=create_autospec(RepositoryFactoryContract),
        third_party_factory=create_autospec(ThirdPartyFactoryContract),
    )


@fixture
def params(faker):
    return HandleNotifyBoletosEvent.from_payload(
        {
            "from_date": int(faker.unix_time()),
            "offset": faker.random_int(0),
            "limit": faker.random_int(100),
        }
    )


def test_event_name(params: HandleNotifyBoletosEvent):
    assert params.get_event_name() == "notifyBoletos"


def test_assert_payload(params: HandleNotifyBoletosEvent):
    assert params.get_payload() == {
        "fromDate": params.from_date,
        "offset": params.offset,
        "limit": params.limit,
    }


def test_not_found_more_boletos(
    sut: HandleNotifyBoletosUsecase,
    params: HandleNotifyBoletosEvent,
    faker,
):
    sut.set_event(params)

    sut.boleto_repository.get_all = MagicMock(
        return_value=PaginatedEntities(
            total_items=faker.random_int(),
            items=[],
        )
    )

    sut.mail.send_simple_mail = MagicMock()
    sut.queue.publish = MagicMock()

    sut.handle()

    sut.mail.send_simple_mail.assert_not_called()
    sut.queue.publish.assert_not_called()

    sut.boleto_repository.get_all.assert_called_once_with(
        limit=params.limit,
        offset=params.offset,
        from_date=params.from_date,
    )


def test_send_emails_and_continue_notifications(
    sut: HandleNotifyBoletosUsecase,
    params: HandleNotifyBoletosEvent,
    faker,
):
    sut.set_event(params)

    total_items = faker.random_int(1, 50)

    sut.boleto_repository.get_all = MagicMock(
        return_value=PaginatedEntities(
            total_items=total_items,
            items=[make_boleto() for _ in range(total_items)],
        )
    )

    sut.mail.send_simple_mail = MagicMock()
    sut.queue.publish = MagicMock()

    sut.handle()

    assert sut.mail.send_simple_mail.call_count == total_items
    sut.queue.publish.assert_called_once()
    sut.boleto_repository.get_all.assert_called_once_with(
        limit=params.limit,
        offset=params.offset - 1,
        from_date=params.from_date,
    )
