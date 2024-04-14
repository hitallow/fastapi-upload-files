from http import HTTPStatus

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.domain.entities.file_import import FileImport
from app.domain.usecases import UploadFromCSVRequest
from app.domain.usecases.import_from_csv import UploadFromCSVResponse
from app.domain.usecases.list_file_imports import (ListFileImportsRequest,
                                                   ListFileImportsResponse)
from app.presentation.factories import (list_file_import_factory,
                                        upload_from_csv_factory)

router = APIRouter(prefix="/file", tags=["Importação de arquivos"])


@router.get(
    "",
    summary="Lista todos os arquivos em importação",
    description="Lista todos os arquivos em importação de forma paginada",
    response_model=ListFileImportsResponse,
    status_code=HTTPStatus.OK,
)
async def list_all_boleto(limit: int = 30, offset: int = 0):
    return list_file_import_factory().execute(
        ListFileImportsRequest(limit=limit, offset=offset)
    )


@router.get(
    "/{file_import_id}",
    summary="Lista importação de arquivo pelo seu id",
    description="Carrega boleto pelo seu identificador unico",
    response_model=FileImport,
    status_code=HTTPStatus.OK,
)
async def list_boleto_by_id(file_import_id: str):
    return list_file_import_factory().execute(
        ListFileImportsRequest(file_import_id=file_import_id)
    )


@router.post(
    "/import",
    summary="Faz o upload do arquivo para sua devida importação",
    description="Inicia o processo de importação de arquivo",
    status_code=HTTPStatus.OK,
    response_model=UploadFromCSVResponse,
)
async def import_from_file_async(
    file: UploadFile = File(description="Arquivo CSV para leitura de dados"),
):
    if file.content_type != "text/csv":
        raise HTTPException(HTTPStatus.BAD_REQUEST, "invalid file type")

    file_in_bytes = await file.read()

    output = upload_from_csv_factory().execute(
        UploadFromCSVRequest(
            file=file_in_bytes,
            filename=file.filename or "not-informed",
            size=file.size or 0,
        ),
    )

    file.file.close()

    return output
