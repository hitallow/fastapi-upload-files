from app.domain.entities.entity import Entity
from app.domain.entities.file import File


class FileImport(Entity):
    id: str | None = None
    title: str
    status: str
    created_at: int = 0
    updated_at: int = 0
    file: File | None = None
