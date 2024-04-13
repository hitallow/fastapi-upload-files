from unittest.mock import MagicMock, create_autospec

from faker import Faker
from pytest import fixture

from app.domain.contracts.repository_factory import RepositoryFactoryContract
from app.domain.entities.boleto import Boleto
from app.domain.entities.paginted_list import PaginatedEntities
from app.domain.usecases.list_boletos import (ListBoletoRequest,
                                              ListBoletoResponse,
                                              ListBoletoUsecase)
from tests.helpers.generate_entities import make_boleto


@fixture
def sut() -> ListBoletoUsecase:
    return ListBoletoUsecase(
        repository_factory=create_autospec(RepositoryFactoryContract),
    )


def test_should_load_all_with_success(sut: ListBoletoUsecase, faker: Faker):
    
    total_items = faker.random_int(1, 100)
    items = [make_boleto() for _ in range(total_items)]

    limit= faker.random_int(1,100)
    offset= faker.random_int(0,100)

    paginated = PaginatedEntities(total_items=total_items, items=items)

    sut.boleto_repository.get_all = MagicMock(return_value=paginated)

    response = sut.execute(ListBoletoRequest(limit=limit, offset=offset))


    assert isinstance(response, ListBoletoResponse)

    assert response.total_items == total_items
    assert len(response.boletos) == len(items)

    sut.boleto_repository.get_all.assert_called_once_with(
        limit=limit,
        offset=offset
    )

def test_should_load_one_by_id(sut: ListBoletoUsecase, faker: Faker):
    
    

    boleto = make_boleto()
    boleto_id = boleto.id

    sut.boleto_repository.get_by_id = MagicMock(return_value=boleto)

    response = sut.execute(ListBoletoRequest(boleto_id=boleto_id))

    assert isinstance(response, Boleto)
    assert response.id == boleto_id
    sut.boleto_repository.get_by_id.assert_called_once_with(boleto_id)
    
