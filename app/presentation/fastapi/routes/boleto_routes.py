from http import HTTPStatus

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.domain.usecases import (ListBoletoRequest, ListBoletoResponse,
                                 UploadFromCSVRequest)
from app.presentation.factories import (list_boleto_factory,
                                        upload_from_csv_factory)

router = APIRouter(prefix="/boleto")


@router.get(
    "",
    summary="Lista todos os boletos",
    description="Lista todos os boletos de forma paginada",
    response_model=ListBoletoResponse,
    status_code=HTTPStatus.OK,
)
async def list_all_boleto(limit: int = 30, offset: int = 0):
    return list_boleto_factory().execute(ListBoletoRequest(limit=limit, offset=offset))


@router.post(
    "/import-from-file",
    summary="Upload arquivos CSV para popular tabela de boletos",
    description="Endpoint multi-thread para upload de aquivos CSV",
    status_code=HTTPStatus.NO_CONTENT,
)
async def import_from_file(
    file: UploadFile = File(description="Arquivo CSV para leitura de dados"),
):
    if file.content_type != "text/csv":
        raise HTTPException(HTTPStatus.BAD_REQUEST, "invalid file type")

    output = upload_from_csv_factory().execute(UploadFromCSVRequest(file=file.file))
    file.file.close()

    return output


@router.post(
    "/import-from-file-async",
    summary="Faz o upload do arquivo e executa o ",
    description="Endpoint multi-thread para upload de aquivos CSV",
    status_code=HTTPStatus.NO_CONTENT,
)
async def import_from_file_async(
    file: UploadFile = File(description="Arquivo CSV para leitura de dados"),
):
    if file.content_type != "text/csv":
        raise HTTPException(HTTPStatus.BAD_REQUEST, "invalid file type")

    output = upload_from_csv_factory().execute(UploadFromCSVRequest(file=file.file))
    file.file.close()

    return output


@router.get(
    "/{boleto_id}",
    summary="Lista todos os boletos",
    description="Lista todos os boletos de forma paginada",
    response_model=ListBoletoResponse,
    status_code=HTTPStatus.OK,
)
async def list_boleto_by_id(boleto_id: int):
    return list_boleto_factory().execute(ListBoletoRequest(boleto_id=boleto_id))
