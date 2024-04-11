from typing import List

from app.domain.contracts.usecase import BaseData, Usecase


class ListBoletoInput(BaseData):
    limit: int
    offset: int


class ListBoletoResponse(BaseData):
    boletos: List


class ListBoletoUsecase(Usecase):

    def execute(self, data: ListBoletoInput) -> ListBoletoResponse:

        return ListBoletoResponse(
            boletos=[
                {"id": 1},
                {"id": 2},
                {"id": 3},
                {"id": 4},
            ]
        )
