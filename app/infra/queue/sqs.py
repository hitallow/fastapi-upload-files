import json

import boto3

from app.domain.contracts.queue import Queue
from app.domain.contracts.queue_event import QueueEvent


class Sqs(Queue):
    _queue_name = "kanastra-imports"

    def __init__(self) -> None:
        self.sqsClient = boto3.client(
            "sqs",
            endpoint_url="http://localstack:4566",
            region_name="sa-east-1",
            aws_access_key_id="foo",
            aws_secret_access_key="000000000000",
        )
        self._create_queue()

    def _create_queue(self):
        try:
            self.sqsClient.get_queue_url(QueueName=self._queue_name)
        except:
            self.sqsClient.create_queue(QueueName=self._queue_name)

    def publish(self, event: QueueEvent):
        self.sqsClient.send_message(
            QueueUrl=self._queue_name,
            MessageBody=json.dumps(
                {
                    "DelaySeconds": event.get_delay_seconds(),
                    "body": json.dumps(
                        {
                            "eventName": event.get_event_name(),
                            "payload": event.get_payload(),
                        }
                    ),
                }
            ),
        )

    def consume(self):
        for message in self.sqsClient.receive_messages():
            print(message)
            message.delete()
