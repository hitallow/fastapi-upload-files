from typing import Dict

from app.domain.contracts.handler import Handler
from app.domain.usecases.handle_import_csv import (HandleImportCSVEvent,
                                                   HandleImportCSVUsecase)
from app.presentation.factories.repository_factory import RepositoryFactory
from app.presentation.factories.third_party_factory import ThirdPartyFactory


def handle_import_csv(event_body: Dict) -> Handler:

    handler = HandleImportCSVUsecase(
        third_party_factory=ThirdPartyFactory(),
        repository_factory=RepositoryFactory(),
    )

    handler.set_event(HandleImportCSVEvent.from_payload(event_body))

    return handler
