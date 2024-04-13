from datetime import datetime

from app.domain.contracts.third_party_factory import ThirdPartyFactoryContract
from app.domain.contracts.usecase import Usecase
from app.domain.entities.entity import Entity
from app.domain.exceptions.publish_queue_task_exception import \
    PublishQueueTaskException
from app.domain.usecases.handle_notify_boletos import HandleNotifyBoletosEvent


class InitNotifyBoletosRequest(Entity):
    pass


class InitNotifyBoletosResponse(Entity):
    pass


class InitNotifyBoletos(Usecase[InitNotifyBoletosRequest, InitNotifyBoletosResponse]):

    def __init__(self, third_party_factory: ThirdPartyFactoryContract) -> None:
        self.logging = third_party_factory.get_logging()
        self.queue = third_party_factory.get_queue()

    def execute(self, data: InitNotifyBoletosRequest) -> InitNotifyBoletosResponse:
        try:
            today = datetime.today()

            self.logging.info(
                f"iniciando leitura dos boletos do dia  {today.strftime('%d/%m/%Y')}"
            )

            today = today.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )

            self.queue.publish(
                HandleNotifyBoletosEvent(from_date=int(today.timestamp()))
            )

            self.logging.info("enfileriado")

        except PublishQueueTaskException as publish_error:
            # notificar alguem via email talvez ....
            self.logging.error("erro ao publicar na fila")

        return InitNotifyBoletosResponse()
