from app.domain.usecases.list_file_imports import ListFileImportsUsecase
from app.presentation.factories.repository_factory import RepositoryFactory


def list_file_import_factory():
    return ListFileImportsUsecase(
        RepositoryFactory()
    )