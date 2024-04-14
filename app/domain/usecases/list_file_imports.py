from typing import List

from app.domain.contracts.repository_factory import RepositoryFactoryContract
from app.domain.contracts.usecase import Usecase
from app.domain.entities.entity import Entity
from app.domain.entities.file_import import FileImport


class ListFileImportsRequest(Entity):
    limit: int | None = 100
    offset: int | None = 0
    file_import_id: str | None = None


class ListFileImportsResponse(Entity):
    total_items: int
    file_imports: List


class ListFileImportsUsecase(Usecase[ListFileImportsRequest, ListFileImportsResponse | FileImport]):

    def __init__(self, repository_factory: RepositoryFactoryContract) -> None:
        self.file_import_repository = repository_factory.get_file_import_repository()

    def execute(self, data: ListFileImportsRequest) -> ListFileImportsResponse | FileImport:

        if data.file_import_id:
            return self.file_import_repository.get_by_id(data.file_import_id)

        page = self.file_import_repository.get_all(
            limit=data.limit,
            offset=data.offset,
        )

        return ListFileImportsResponse(
            total_items=page.total_items,
            file_imports=page.items,
        )
