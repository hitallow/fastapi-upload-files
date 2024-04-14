from http import HTTPStatus

from fastapi import APIRouter

from app.domain.entities.boleto import Boleto
from app.domain.usecases import ListBoletoRequest, ListBoletoResponse
from app.presentation.factories import list_boleto_factory

router = APIRouter(prefix="/boleto", tags=['Boletos'])


@router.get(
    "",
    summary="Lista todos os boletos",
    description="Lista todos os boletos de forma paginada",
    response_model=ListBoletoResponse,
    status_code=HTTPStatus.OK,
)
async def list_all_boleto(limit: int = 30, offset: int = 0):
    return list_boleto_factory().execute(ListBoletoRequest(limit=limit, offset=offset))


@router.get(
    "/{boleto_id}",
    summary="Lista boleto pelo seu id",
    description="Carrega boleto pelo seu identificador unico",
    response_model=Boleto,
    status_code=HTTPStatus.OK,
)
async def list_boleto_by_id(boleto_id: str):
    return list_boleto_factory().execute(ListBoletoRequest(boleto_id=boleto_id))
