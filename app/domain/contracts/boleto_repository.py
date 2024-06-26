from abc import ABC, abstractmethod
from typing import List, Tuple

from app.domain.entities.boleto import Boleto
from app.domain.entities.paginted_list import PaginatedEntities


class BoletoRepositoryContract(ABC):

    @abstractmethod
    def insert_one(self, boleto: Boleto) -> Boleto:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: str) -> Boleto:
        raise NotImplementedError

    @abstractmethod
    def insert_many(self, boletos: List[Boleto]) -> List[Boleto]:
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self, 
        limit: int | None = None, 
        offset: int | None = None,
        from_date: int | None = None,
    ) -> PaginatedEntities[Boleto]:
        raise NotImplementedError
