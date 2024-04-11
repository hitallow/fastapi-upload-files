from fastapi import APIRouter

from app.domain.usecases.list_boletos import ListBoletoInput
from app.presentation.factories import list_boleto_factory

router = APIRouter(prefix='/boleto')


@router.get('')
async def list_all_boleto():
    return list_boleto_factory().execute(
        ListBoletoInput(
            limit=10,
            offset=0
        )
    )