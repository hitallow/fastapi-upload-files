from app.domain.contracts.queue import Queue
from app.domain.contracts.storage import Storage
from app.domain.contracts.third_party_factory import ThirdPartyFactoryContract


class ThirdPartyFactory(ThirdPartyFactoryContract):

    _queue: Queue | None = None
    _storage: Storage | None = None

    def get_queue(self) -> Queue:

        if not self._queue:
            from app.infra.queue.sqs import Sqs

            self._queue = Sqs()
        return self._queue

    def get_storage(self) -> Storage:
        if not self._storage:
            from app.infra.storage.s3 import S3

            self._storage = S3()

        return self._storage
