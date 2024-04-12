from app.domain.usecases.list_boletos import ListBoletoUsecase
from app.presentation.factories.repository_factory import RepositoryFactory


def list_boleto_factory() -> ListBoletoUsecase:
    return ListBoletoUsecase(
        repository_factory=RepositoryFactory(),
    )
