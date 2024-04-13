from typing import Dict

from app.domain.contracts.handler import Handler
from app.domain.usecases.handle_notify_boletos import (
    HandleNotifyBoletosEvent, HandleNotifyBoletosUsecase)
from app.presentation.factories.repository_factory import RepositoryFactory
from app.presentation.factories.third_party_factory import ThirdPartyFactory


def handle_notify_boletos_factory(event_body: Dict) -> Handler:

    handler = HandleNotifyBoletosUsecase(
        third_party_factory=ThirdPartyFactory(),
        repository_factory=RepositoryFactory(),
    )

    handler.set_event(HandleNotifyBoletosEvent.from_payload(event_body))

    return handler
