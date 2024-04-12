from app.domain.usecases.import_from_csv import UploadFromCSVUsecase
from app.presentation.factories.repository_factory import RepositoryFactory
from app.presentation.factories.third_party_factory import ThirdPartyFactory


def upload_from_csv_factory():

    return UploadFromCSVUsecase(
        third_party_factory=ThirdPartyFactory(),
        repository_factory=RepositoryFactory(),
    )
