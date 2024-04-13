from datetime import datetime
from unittest.mock import MagicMock, create_autospec

from pytest import fixture

from app.domain.contracts.third_party_factory import ThirdPartyFactoryContract
from app.domain.usecases.handle_notify_boletos import HandleNotifyBoletosEvent
from app.domain.usecases.init_notify_boletos import (InitNotifyBoletos,
                                                     InitNotifyBoletosRequest)


@fixture
def sut() -> InitNotifyBoletos:
    return InitNotifyBoletos(
        third_party_factory=create_autospec(ThirdPartyFactoryContract)
    )


def test_should_execute_with_success(sut: InitNotifyBoletos):

    sut.logging.info = MagicMock()
    sut.queue.publish = MagicMock()

    sut.execute(InitNotifyBoletosRequest())

    sut.logging.info.assert_called()
    sut.queue.publish.assert_called_once_with(
        HandleNotifyBoletosEvent(
            from_date=int(
                datetime.today()
                .replace(
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                )
                .timestamp()
            )
        )
    )
