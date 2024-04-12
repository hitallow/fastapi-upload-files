import logging

from app.domain.contracts.logging import Logging as LoggingContract


class Logging(LoggingContract):

    def __init__(self) -> None:
        logging.basicConfig(
            format="%(asctime)s: %(levelname)s: %(message)s", level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)

    def info(self, info) -> None:
        self.logger.info(info)

    def error(self, error) -> None:
        self.logger.error(error)

    def debug(self, debug) -> None:
        self.logger.debug(debug)
