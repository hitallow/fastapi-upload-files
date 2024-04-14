from unittest.mock import MagicMock, create_autospec

from faker import Faker
from pytest import fixture

from app.domain.contracts.repository_factory import RepositoryFactoryContract
from app.domain.entities.file_import import FileImport
from app.domain.entities.paginted_list import PaginatedEntities
from app.domain.usecases.list_file_imports import (ListFileImportsRequest,
                                                   ListFileImportsResponse,
                                                   ListFileImportsUsecase)
from tests.helpers.generate_entities import make_file_import


@fixture
def sut() -> ListFileImportsUsecase:
    return ListFileImportsUsecase(
        repository_factory=create_autospec(RepositoryFactoryContract),
    )


def test_should_load_all_with_success(sut: ListFileImportsUsecase, faker: Faker):
    
    total_items = faker.random_int(1, 100)
    items = [make_file_import() for _ in range(total_items)]

    limit= faker.random_int(1,100)
    offset= faker.random_int(0,100)

    paginated = PaginatedEntities(total_items=total_items, items=items)

    sut.file_import_repository.get_all = MagicMock(return_value=paginated)

    response = sut.execute(ListFileImportsRequest(limit=limit, offset=offset))


    assert isinstance(response, ListFileImportsResponse)

    assert response.total_items == total_items
    assert len(response.file_imports) == len(items)

    sut.file_import_repository.get_all.assert_called_once_with(
        limit=limit,
        offset=offset
    )

def test_should_load_one_by_id(sut: ListFileImportsUsecase, faker: Faker):
    file_import = make_file_import()
    file_import_id = file_import.id

    sut.file_import_repository.get_by_id = MagicMock(return_value=file_import)

    response = sut.execute(ListFileImportsRequest(file_import_id=file_import_id))

    assert isinstance(response, FileImport)
    assert response.id == file_import_id
    sut.file_import_repository.get_by_id.assert_called_once_with(file_import_id)
    
