from typing import List, Tuple
from uuid import uuid4

from app.domain.contracts import BoletoRepositoryContract
from app.domain.entities import Boleto
from app.domain.entities.paginted_list import PaginatedEntities
from app.infra.database.connection import Connection


class BoletoRepository(BoletoRepositoryContract):

    def __init__(self) -> None:
        self.db = Connection().get_database()

    def insert_one(self, boleto: Boleto) -> Boleto:

        boleto_id = str(uuid4())

        with Connection().get_new_connection() as db:
            db.cursor().execute(
                "INSERT INTO boleto (id, name, debitId, governmentId, email, debitAmount, dueDate) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    boleto_id,
                    boleto.name,
                    boleto.debit_id,
                    boleto.government_id,
                    boleto.email,
                    boleto.debit_amount,
                    boleto.due_date,
                ),
            )
            db.commit()
        boleto.id = boleto_id

        return boleto

    def insert_many(self, boletos: List[Boleto]) -> List[Boleto]:

        with Connection().get_new_connection() as db:
            db.executemany(
                "INSERT INTO boleto (id, name, debitId, governmentId, email, debitAmount, dueDate) VALUES (?, ?, ?, ?, ?, ?, ?)",
                [
                    (
                        str(uuid4()),
                        boleto.name,
                        boleto.debit_id,
                        boleto.government_id,
                        boleto.email,
                        boleto.debit_amount,
                        boleto.due_date,
                    )
                    for boleto in boletos
                ],
            )
            db.commit()

        return boletos

    def __count_all_items(self) -> int:
        r = self.db.execute("select count(*) as total from boleto;").fetchone()
        return r[0]

    def get_all(
        self,
        limit: int | None = None,
        offset: int | None = None,
        from_date: int | None = None,
    ) -> PaginatedEntities[Boleto]:

        sql = "select id, name, debitId, governmentId, email, debitAmount, dueDate from boleto"

        if from_date is not None:
            sql = f"{sql} WHERE dueDate = {from_date}"

        if limit is not None and offset is not None:
            sql = f"{sql} LIMIT {limit} OFFSET {offset * limit}"

        boletos = [
            Boleto(
                id=db_data[0],
                name=db_data[1],
                debit_id=db_data[2],
                government_id=db_data[3],
                email=db_data[4],
                debit_amount=db_data[5],
                due_date=db_data[6],
            )
            for db_data in self.db.execute(sql).fetchall()
        ]
        return PaginatedEntities(total_items=self.__count_all_items(), items=boletos)

    def get_by_id(self, id: str) -> Boleto:
        raise Exception
