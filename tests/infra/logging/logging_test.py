from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from app.infra.logging.logging import Logging


@pytest.mark.parametrize(
    "method",
    [
        ("info"),
        ("error"),
        ("debug"),
    ],
)
def test_should_log_info(method: str, faker):
    class FakeLogger:
        pass

    fake_logger = FakeLogger()

    fn = MagicMock()
    setattr(fake_logger, method, fn)
    with patch("app.infra.logging.logging.logging.getLogger", return_value=fake_logger):
        logging = Logging()

    message = faker.word()

    getattr(logging, method)(message)

    fn.assert_called_once_with(message)
