from app.domain.usecases.list_boletos import ListBoletoUsecase
from app.infra.database.repositories import BoletoRepository


def list_boleto_factory() -> ListBoletoUsecase:
    return ListBoletoUsecase(
        boleto_repository=BoletoRepository()
    )
