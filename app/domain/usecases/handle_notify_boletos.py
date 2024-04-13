from typing import Dict

from app.domain.contracts.handler import Handler
from app.domain.contracts.queue_event import QueueEvent
from app.domain.contracts.repository_factory import RepositoryFactoryContract
from app.domain.contracts.third_party_factory import ThirdPartyFactoryContract
from app.domain.entities.entity import Entity


class HandleNotifyBoletosEvent(QueueEvent, Entity):
    from_date: int
    offset: int = 0
    limit: int = 100

    def get_event_name(self) -> str:
        return "notifyBoletos"

    def get_payload(self) -> Dict:
        return self.model_dump(by_alias=True)

    @staticmethod
    def from_payload(event: Dict) -> "HandleNotifyBoletosEvent":
        return HandleNotifyBoletosEvent(**event)


class HandleNotifyBoletosUsecase(Handler):
    _event: HandleNotifyBoletosEvent

    def __init__(
        self,
        repository_factory: RepositoryFactoryContract,
        third_party_factory: ThirdPartyFactoryContract,
    ) -> None:
        self.boleto_repository = repository_factory.get_boleto_repository()
        self.queue = third_party_factory.get_queue()
        self.logging = third_party_factory.get_logging()
        self.mail = third_party_factory.get_mail()

    def set_event(self, event: HandleNotifyBoletosEvent):
        self._event = event

    def handle(self):
        boletos = self.boleto_repository.get_all(
            limit=self._event.limit,
            offset=self._event.offset,
            from_date=self._event.from_date
        ).items

        if not boletos:
            self.logging.info("nada mais para notificar, parando")
            return

        self.logging.info(f"notificando {len(boletos)} boletos")

        for boleto in boletos:
            self.mail.send_simple_mail(
                to=[boleto.email],
                subject="Boleto para hoje!",
                message=f"""
                    Olá {boleto.name},

                    Há um boleto no valor de R$ {(boleto.debit_amount / 100):.2f} agendado para hoje.
                    Certifique-se de fazer o pagamento para não ficar em atraso

                    Em caso de dúvidas, é só entrar em contato com nossa empresa.

                    Att, Equipe Kanastra.""",
            )

        self._event.offset = self._event.offset + 1

        self.logging.info('enfileirando novamente para enviar...')

        self.queue.publish(self._event)
