from abc import ABC, abstractmethod
from typing import List


class Mail(ABC):
    @abstractmethod
    def send_simple_mail(
        self,
        to: List[str],
        subject: str,
        message: str
    ) -> bool:
        raise NotImplementedError()