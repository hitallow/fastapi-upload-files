import json
from typing import Any, Dict
from unittest.mock import MagicMock, call, create_autospec, patch

import pytest

from app.domain.contracts.handler import Handler
from app.domain.contracts.logging import Logging
from app.domain.contracts.queue_event import QueueEvent
from app.domain.exceptions.publish_queue_task_exception import \
    PublishQueueTaskException
from app.infra.queue.sqs import Sqs
from tests.helpers.fake_aws_client import FakeAwsClient


@pytest.fixture
def sut():
    with patch("boto3.client", return_value=FakeAwsClient()):
        yield Sqs(create_autospec(Logging))


class FakeEvent(QueueEvent):
    def __init__(
        self, event_name: str = "anyEvent", payload: Dict = {}, delay: int = 0
    ) -> None:
        self.event_name = event_name
        self.payload = payload
        self.delay = delay

    def get_event_name(self) -> str:
        return self.event_name

    def get_payload(self) -> Any:
        return self.payload

    def get_delay_seconds(self) -> int:
        return self.delay

    @staticmethod
    def from_payload():
        return FakeEvent()


class FakeHandler(Handler):
    def set_event(self, event: QueueEvent):
        pass

    def handle(self):
        pass


def test_init_and_get_a_created_queue():
    fake_aws = FakeAwsClient()
    fake_aws.get_queue_url = MagicMock()
    fake_aws.create_queue = MagicMock()

    with patch("boto3.client", return_value=fake_aws):
        Sqs(create_autospec(Logging))

    fake_aws.get_queue_url.assert_called_once_with(QueueName=Sqs._queue_name)
    fake_aws.create_queue.assert_not_called()


def test_init_and_create_a_queue():
    fake_aws = FakeAwsClient()
    fake_aws.create_queue = MagicMock()
    fake_aws.get_queue_url = MagicMock(side_effect=Exception)

    with patch("boto3.client", return_value=fake_aws):
        Sqs(create_autospec(Logging))

    fake_aws.get_queue_url.assert_called_once_with(QueueName=Sqs._queue_name)
    fake_aws.create_queue.assert_called_once_with(QueueName=Sqs._queue_name)


def test_should_get_error_on_publish_task(faker):
    fake_aws = FakeAwsClient()
    fake_aws.send_message = MagicMock(side_effect=Exception)

    with patch("boto3.client", return_value=fake_aws):
        sqs = Sqs(create_autospec(Logging))

    event_name = faker.word()
    payload = {faker.word(): faker.word()}

    delay = faker.random_int(min=10)

    event = FakeEvent(event_name=event_name, payload=payload, delay=delay)

    with pytest.raises(PublishQueueTaskException):
        sqs.publish(event)

    fake_aws.send_message.assert_called_once_with(
        QueueUrl=sqs._queue_name,
        DelaySeconds=event.get_delay_seconds(),
        MessageBody=json.dumps(
            {
                "DelaySeconds": event.get_delay_seconds(),
                "eventName": event.get_event_name(),
                "payload": json.dumps(
                    event.get_payload(),
                ),
            }
        ),
    )


def test_should_publish_task_with_success(faker):
    fake_aws = FakeAwsClient()
    fake_aws.send_message = MagicMock()

    with patch("boto3.client", return_value=fake_aws):
        sqs = Sqs(create_autospec(Logging))

    event_name = faker.word()
    payload = {faker.word(): faker.word()}

    delay = faker.random_int(min=10)

    event = FakeEvent(event_name=event_name, payload=payload, delay=delay)

    sqs.publish(event)

    fake_aws.send_message.assert_called_once_with(
        QueueUrl=sqs._queue_name,
        DelaySeconds=event.get_delay_seconds(),
        MessageBody=json.dumps(
            {
                "DelaySeconds": event.get_delay_seconds(),
                "eventName": event.get_event_name(),
                "payload": json.dumps(
                    event.get_payload(),
                ),
            }
        ),
    )


def test_should_not_found_messages_to_consume(sut: Sqs):

    sut.sqsClient.receive_message = MagicMock(return_value={})
    sut.logging.info = MagicMock()

    sut.consume()

    sut.sqsClient.receive_message.assert_called_once_with(QueueUrl=Sqs._queue_name)
    sut.logging.info.assert_called_once_with("nothing to read")


def test_should_not_found_handler(sut: Sqs, faker):
    event_name = faker.word()
    payload = {faker.word(): faker.word()}
    sut.sqsClient.receive_message = MagicMock(
        return_value={
            "Messages": [
                {
                    "Body": json.dumps(
                        {
                            "eventName": event_name,
                            "payload": json.dumps(payload),
                        }
                    )
                }
            ]
        }
    )

    sut.logging.info = MagicMock()
    with patch("app.infra.queue.sqs.sqs_handler_factory") as factory_handler:
        factory_handler.return_value = None
        sut.consume()

    factory_handler.assert_called_once_with(event_name, payload)

    sut.sqsClient.receive_message.assert_called_once_with(QueueUrl=Sqs._queue_name)
    sut.logging.info.assert_has_calls(
        [
            call(f"reading {event_name}"),
            call("not found an handler"),
        ]
    )


def test_should_get_error_on_execute_handler(sut: Sqs, faker):
    event_name = faker.word()
    payload = {faker.word(): faker.word()}
    sut.sqsClient.receive_message = MagicMock(
        return_value={
            "Messages": [
                {
                    "Body": json.dumps(
                        {
                            "eventName": event_name,
                            "payload": json.dumps(payload),
                        }
                    )
                }
            ]
        }
    )

    sut.logging.info = MagicMock()
    sut.logging.error = MagicMock()

    fake_handle = FakeHandler()

    fake_handle.handle = MagicMock(side_effect=Exception)

    with patch("app.infra.queue.sqs.sqs_handler_factory") as factory_handler:
        factory_handler.return_value = fake_handle
        sut.consume()


    fake_handle.handle.assert_called_once()
    factory_handler.assert_called_once_with(event_name, payload)
    sut.sqsClient.receive_message.assert_called_once_with(QueueUrl=Sqs._queue_name)
    sut.logging.info.assert_has_calls(
        [
            call(f"reading {event_name}"),
            call("executing handler"),
        ]
    )
    sut.logging.error.assert_called_once()

def test_should_execute_with_success(sut: Sqs, faker):
    event_name = faker.word()
    receipt_handle = faker.word()
    payload = {faker.word(): faker.word()}
    sut.sqsClient.receive_message = MagicMock(
        return_value={
            "Messages": [
                {
                    'ReceiptHandle': receipt_handle,
                    "Body": json.dumps(
                        {
                            "eventName": event_name,
                            "payload": json.dumps(payload),
                        }
                    )
                }
            ]
        }
    )

    sut.logging.info = MagicMock()
    sut.logging.error = MagicMock()

    fake_handle = FakeHandler()

    fake_handle.handle = MagicMock()
    sut.sqsClient.delete_message = MagicMock()

    with patch("app.infra.queue.sqs.sqs_handler_factory") as factory_handler:
        factory_handler.return_value = fake_handle
        sut.consume()

    factory_handler.assert_called_once_with(event_name, payload)
    fake_handle.handle.assert_called_once()

    sut.sqsClient.receive_message.assert_called_once_with(QueueUrl=Sqs._queue_name)
    sut.sqsClient.delete_message.assert_called_once_with(
        QueueUrl=Sqs._queue_name,
        ReceiptHandle=receipt_handle
    )
    sut.logging.info.assert_has_calls(
        [
            call(f"reading {event_name}"),
            call("executing handler"),
        ]
    )
    sut.logging.error.assert_not_called()
