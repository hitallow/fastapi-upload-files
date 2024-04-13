from app.domain.contracts.usecase import Usecase
from app.domain.usecases.init_notify_boletos import InitNotifyBoletos
from app.presentation.factories.third_party_factory import ThirdPartyFactory


def init_notify_boletos_factory() -> Usecase:
    return InitNotifyBoletos(
        third_party_factory=ThirdPartyFactory()
    )