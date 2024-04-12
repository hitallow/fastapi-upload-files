from typing import Any

from app.domain.entities.entity import Entity


class File(Entity):
    id: str | None = None
    filename: str
    orignalFilename: str
    size: float
    # when file is charged from storage, its saved here
    tempFile: Any | None = None
