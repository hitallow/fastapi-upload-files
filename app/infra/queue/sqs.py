import json

import boto3

from app.domain.contracts.queue import Queue
from app.domain.contracts.queue_event import QueueEvent
from app.presentation.factories.sqs_handler_factory import sqs_handler_factory


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
                    "eventName": event.get_event_name(),
                    "payload": json.dumps(
                        event.get_payload(),
                    ),
                }
            ),
        )

    def consume(self):
        response = self.sqsClient.receive_message(QueueUrl=self._queue_name)
        if "Messages" in response:
            for message in response["Messages"]:
                message_body = json.loads(message["Body"])
                event_name = message_body["eventName"]
                print(f"doing {event_name}")
                payload = json.loads(message_body["payload"])

                handler = sqs_handler_factory(event_name, payload)

                if handler:
                    handler.handle()

                self.sqsClient.delete_message(
                    QueueUrl=self._queue_name,
                    ReceiptHandle=message["ReceiptHandle"],
                )
        else:
            print("nothing to read")
