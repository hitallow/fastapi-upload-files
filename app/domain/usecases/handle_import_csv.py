import csv
from datetime import datetime
from io import StringIO
from typing import Dict, List

from app.domain.contracts import Handler, QueueEvent
from app.domain.contracts.repository_factory import RepositoryFactoryContract
from app.domain.contracts.third_party_factory import ThirdPartyFactoryContract
from app.domain.entities.boleto import Boleto
from app.domain.entities.entity import Entity
from app.domain.exceptions.file_not_found_exception import \
    FileNotFoundException
from app.domain.exceptions.publish_queue_task_exception import \
    PublishQueueTaskException


class HandleImportCSVEvent(QueueEvent, Entity):
    file_import_id: str
    filename: str
    target: int = 0
    lines: int = 1000

    def get_payload(self) -> Dict:
        return {
            "fileImportId": self.file_import_id,
            "filename": self.filename,
            "target": self.target,
            "lines": self.lines,
        }

    def get_event_name(self) -> str:
        return "importBoletosFromCSV"

    @staticmethod
    def from_payload(event: Dict) -> "HandleImportCSVEvent":
        return HandleImportCSVEvent(
            file_import_id=event["fileImportId"],
            filename=event["filename"],
            target=event["target"],
            lines=event["lines"],
        )


class HandleImportCSVUsecase(Handler):

    _event: HandleImportCSVEvent

    def __init__(
        self,
        repository_factory: RepositoryFactoryContract,
        third_party_factory: ThirdPartyFactoryContract,
    ) -> None:
        self.boleto_repository = repository_factory.get_boleto_repository()
        self.file_import_repository = repository_factory.get_file_import_repository()
        self.file_repository = repository_factory.get_file_repository()
        self.storage = third_party_factory.get_storage()
        self.queue = third_party_factory.get_queue()
        self.logger = third_party_factory.get_logging()

    def set_event(self, event: HandleImportCSVEvent):
        self._event = event

    def _storage_lines(self, rows: List[Dict[str, str]]):
        boletos = []
        for row in rows:
            boletos.append(
                Boleto(
                    name=row["name"],
                    debit_amount=int(row["debtAmount"]),
                    email=row["email"],
                    government_id=row["governmentId"],
                    debit_id=row["debtId"],
                    due_date=int(
                        datetime.strptime(row["debtDueDate"], "%Y-%m-%d").timestamp()
                    ),
                )
            )

        self.boleto_repository.insert_many(boletos)

    def _get_slice_of_file(
        self,
    ) -> List[Dict[str, str]]:

        file = self.storage.load(self._event.filename)

        target = self._event.target
        lines = self._event.lines

        return list(csv.DictReader(StringIO(file.decode()), delimiter=","))[
            target : target + lines
        ]

    def handle(self):

        try:
            self.logger.info(
                f"iniciando processamento, iniciando da linha {self._event.target}"
            )
            rows = self._get_slice_of_file()

            if not rows:
                self.logger.info("processamento finalizado com sucesso ...")
                self.file_import_repository.update_status(
                    self._event.file_import_id, "done"
                )

                return

            self._storage_lines(rows)

            self._event.target = self._event.target + self._event.lines

            self.logger.info("enfileirando proxima leitura ...")

            self.queue.publish(self._event)
        except FileNotFoundException:
            self.logger.error("arquivo nao encontrado.")
            self.file_import_repository.update_status(
                self._event.file_import_id, "error"
            )

        except PublishQueueTaskException:
            self.logger.error("erro ao publicar.")
            self.file_import_repository.update_status(
                self._event.file_import_id, "error"
            )

        except Exception as error:
            self.logger.error({"message": "ops, erro interno", "error": error})
            self.file_import_repository.update_status(
                self._event.file_import_id, "error"
            )
