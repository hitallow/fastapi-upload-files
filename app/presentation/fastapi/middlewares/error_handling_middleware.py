from http import HTTPStatus
from typing import Any

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction
from starlette.types import ASGIApp

from app.domain.exceptions.entity_not_found_exception import \
    EntityNotFoundException
from app.domain.exceptions.publish_queue_task_exception import \
    PublishQueueTaskException
from app.domain.exceptions.upload_file_exception import UploadFileException
from app.infra.logging.logging import Logging


class ErrorHandlingMiddleware(BaseHTTPMiddleware):

    def __init__(self, app) -> None:
        super().__init__(app)
        self.logging = Logging()

    async def dispatch(self, request: Request, call_next: Any) -> Any:
        try:
            return await call_next(request)

        except EntityNotFoundException as error:
            self.logging.debug(f"entity not found {error}")
            return JSONResponse(
                status_code=HTTPStatus.NOT_FOUND,
                content={
                    "message": error.message,
                },
            )
        except (PublishQueueTaskException, UploadFileException) as error:
            self.logging.error(f"getting error = {error}")
            return JSONResponse(
                status_code=HTTPStatus.BAD_GATEWAY,
                content={
                    "message": "local error, please contact support",
                },
            )
        except Exception as error:
            self.logging.error(f"generic exception = {error}")
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={
                    "message": "internal error",
                },
            )
