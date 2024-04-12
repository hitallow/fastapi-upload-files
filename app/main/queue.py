from time import sleep

from app.infra.logging.logging import Logging
from app.infra.queue.sqs import Sqs

if __name__ == "__main__":
    print("starting ...")
    sqs = Sqs(Logging())

    while True:
        sqs.consume()
        sleep(5)
