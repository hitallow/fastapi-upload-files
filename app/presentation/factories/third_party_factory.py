from app.domain.contracts.logging import Logging
from app.domain.contracts.queue import Queue
from app.domain.contracts.storage import Storage
from app.domain.contracts.third_party_factory import ThirdPartyFactoryContract


class ThirdPartyFactory(ThirdPartyFactoryContract):

    _queue: Queue | None = None
    _storage: Storage | None = None
    _logging: Logging | None = None

    def get_queue(self) -> Queue:

        if not self._queue:
            from app.infra.queue.sqs import Sqs
            self._queue = Sqs(self.get_logging())
        return self._queue

    def get_storage(self) -> Storage:
        if not self._storage:
            from app.infra.storage.s3 import S3

            self._storage = S3()

        return self._storage

    def get_logging(self) -> Logging:
        if not self._logging:
            from app.infra.logging.logging import Logging

            self._logging = Logging()
        return self._logging
