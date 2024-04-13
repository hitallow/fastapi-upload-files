from typing import Dict

from app.domain.contracts.handler import Handler
from app.presentation.factories.handle_import_csv_factory import \
    handle_import_csv
from app.presentation.factories.handle_notify_boletos_factory import \
    handle_notify_boletos_factory


def sqs_handler_factory(event_name: str, event_body: Dict) -> Handler | None:
    if event_name == "importBoletosFromCSV":
        return handle_import_csv(event_body)

    if event_name == 'notifyBoletos':
        return handle_notify_boletos_factory(event_body)
