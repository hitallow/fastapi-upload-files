from app.domain.entities.entity import Entity


class Boleto(Entity):
    id: str
    name: str
    debit_id: str
    government_id: str
    email: str
    debit_amount: int
    due_date: int
