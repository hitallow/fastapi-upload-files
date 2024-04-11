from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.boleto import Boleto


class BoletoRepositoryContract(ABC):

    @abstractmethod
    def insert_one(self, boleto: Boleto) -> Boleto:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: str) -> Boleto:
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self, limit: int | None = None, offset: int | None = None
    ) -> List[Boleto]:
        raise NotImplementedError
