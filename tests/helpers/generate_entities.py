from faker import Faker

from app.domain.entities.boleto import Boleto
from app.domain.entities.file import File
from app.domain.entities.file_import import FileImport

faker = Faker("pt_BR")


def make_boleto() -> Boleto:
    return Boleto(
        id=faker.uuid4(),
        name=faker.first_name(),
        debit_id=faker.bothify("########"),
        government_id=faker.bothify("########"),
        email=faker.email(),
        debit_amount=faker.random_int(10),
        due_date=int(faker.unix_time()),
    )


def make_file():
    return File(
        id=faker.uuid4(),
        filename=faker.file_name(),
        orignalFilename=faker.file_name(),
        size=faker.random_int(100),
    )


def make_file_import():
    return FileImport(
        id=faker.uuid4(),
        title=faker.word(),
        status=faker.word(),
        created_at=int(faker.unix_time()),
        updated_at=int(faker.unix_time()),
        file=make_file(),
    )
