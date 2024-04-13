from faker import Faker

from app.domain.entities.boleto import Boleto

faker = Faker('pt_BR')

def make_boleto() -> Boleto:
    return Boleto(
        id=faker.uuid4(),
        name=faker.first_name(),
        debit_id=faker.bothify('########'),
        government_id=faker.bothify('########'),
        email=faker.email(),
        debit_amount=faker.random_int(10),
        due_date=int(faker.unix_time())
    )