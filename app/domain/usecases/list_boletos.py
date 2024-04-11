from typing import List

from app.domain.contracts.boleto_repository import BoletoRepositoryContract
from app.domain.contracts.usecase import BaseData, Usecase


class ListBoletoRequest(BaseData):
    limit: int | None = 100
    offset: int | None = 0
    boleto_id: int | None = None


class ListBoletoResponse(BaseData):
    total_items: int
    boletos: List


class ListBoletoUsecase(Usecase):

    def __init__(self, boleto_repository: BoletoRepositoryContract) -> None:
        self.boleto_repository = boleto_repository

    def execute(self, data: ListBoletoRequest) -> ListBoletoResponse:

        boletos = self.boleto_repository.get_all(limit=data.limit, offset=data.offset)
        return ListBoletoResponse(
            total_items=len(boletos),
            boletos=boletos,
        )
