from typing import List

from app.domain.contracts.repository_factory import RepositoryFactoryContract
from app.domain.contracts.usecase import Usecase
from app.domain.entities.boleto import Boleto
from app.domain.entities.entity import Entity


class ListBoletoRequest(Entity):
    limit: int | None = 100
    offset: int | None = 0
    boleto_id: str | None = None


class ListBoletoResponse(Entity):
    total_items: int
    boletos: List


class ListBoletoUsecase(Usecase[ListBoletoRequest, ListBoletoResponse | Boleto]):

    def __init__(self, repository_factory: RepositoryFactoryContract) -> None:
        self.boleto_repository = repository_factory.get_boleto_repository()

    def execute(self, data: ListBoletoRequest) -> ListBoletoResponse | Boleto:

        if data.boleto_id:
            return self.boleto_repository.get_by_id(data.boleto_id)

        page = self.boleto_repository.get_all(
            limit=data.limit,
            offset=data.offset,
        )

        return ListBoletoResponse(
            total_items=page.total_items,
            boletos=page.items,
        )
