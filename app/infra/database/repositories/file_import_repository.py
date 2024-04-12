from datetime import datetime
from time import time
from typing import List, Tuple
from uuid import uuid4

from app.domain.contracts import FileImportRepositoryContract
from app.domain.entities import FileImport
from app.infra.database.connection import Connection


class FileImportRepository(FileImportRepositoryContract):
    def __init__(self) -> None:
        self.db = Connection().get_database()

    def insert_one(self, file_import: FileImport) -> FileImport:

        file_import.id = str(uuid4())

        self.db.cursor().execute(
            "INSERT INTO fileImport (id, title, status, fileId) VALUES (?, ?, ?, ?)",
            (
                file_import.id,
                file_import.title,
                file_import.status,
                file_import.file.id if file_import.file else None,
            ),
        )

        self.db.commit()

        return file_import

    def get_by_id(self, id: str) -> FileImport:
        sql = "SELECT id, title, status, createdAt, updatedAt FROM fileImport  WHERE id = ?"
        reply = self.db.execute(sql, (id,)).fetchone()

        return FileImport(
            id=reply[0],
            title=reply[1],
            status=reply[2],
            created_at=int(
                datetime.strptime(reply[3], "%Y-%m-%d %H:%M:%S").timestamp()
            ),
            updated_at=int(
                datetime.strptime(reply[4], "%Y-%m-%d %H:%M:%S").timestamp()
            ),
        )

    def update_status(self, id: str, status: str) -> FileImport:
        sql = "UPDATE fileImport SET status = ?, updatedAt = CURRENT_TIMESTAMP WHERE id = ?"
        self.db.execute(sql, (status, id))
        self.db.commit()
        return self.get_by_id(id)
