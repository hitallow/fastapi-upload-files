from app.domain.usecases.list_boletos import ListBoletoUsecase


def list_boleto_factory() -> ListBoletoUsecase:
    return ListBoletoUsecase()
