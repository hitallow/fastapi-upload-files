import codecs
import csv
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List

from fastapi import HTTPException

from app.domain.contracts.boleto_repository import BoletoRepositoryContract
from app.domain.contracts.usecase import BaseData, Usecase
from app.domain.entities.boleto import Boleto


class UploadFromCSVRequest(BaseData):
    file: Any


class UploadFromCSVResponse(BaseData):
    pass


class UploadFromCSVUsecase(Usecase[UploadFromCSVRequest, UploadFromCSVResponse]):

    def __init__(self, boleto_repository: BoletoRepositoryContract) -> None:
        self.boleto_repository = boleto_repository

    def _handle_data(self, rows: List[Dict[str, str]]):
        try:
            boletos = []
            for row in rows:
                boletos.append(
                    Boleto(
                        id="Olá",
                        name=row["name"],
                        debit_amount=int(row["debtAmount"]),
                        email=row["email"],
                        government_id=row["governmentId"],
                        debit_id=row["debtId"],
                        due_date=1,
                    )
                )

            self.boleto_repository.insert_many(boletos)
        except Exception as e:
            print("houve um erro meu camarada")
            print(e)

    def _break_in_chunks(self, lista, partes=4):
        tamanho_parte = len(lista) // partes
        resto = len(lista) % partes
        n = []
        inicio = 0
        for i in range(partes):
            tamanho = tamanho_parte + (1 if i < resto else 0)
            n.append(lista[inicio : inicio + tamanho])
            inicio += tamanho
        return n

    def _save_in_parallel(self, rows: List):
        threads = 8 if len(rows) >= 100 else 2
        chunks = self._break_in_chunks(rows, threads)

        with ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(self._handle_data, chunks)

    def execute(self, data: UploadFromCSVRequest) -> UploadFromCSVResponse:
        rows = list(csv.DictReader(codecs.iterdecode(data.file, "utf-8")))

        if len(rows) > 5 * 1000:
            raise HTTPException(
                status_code=400, detail="File too large, please use async route"
            )

        self._save_in_parallel(rows)

        return UploadFromCSVResponse()
