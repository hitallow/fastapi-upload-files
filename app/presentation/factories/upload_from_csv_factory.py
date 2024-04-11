from app.domain.usecases.import_from_csv import UploadFromCSVUsecase
from app.infra.database.repositories import BoletoRepository


def upload_from_csv_factory():
    return UploadFromCSVUsecase(boleto_repository=BoletoRepository())
