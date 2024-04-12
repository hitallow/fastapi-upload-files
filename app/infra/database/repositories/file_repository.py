from typing import List, Tuple
from uuid import uuid4

from app.domain.contracts import FileRepositoryContract
from app.domain.entities import File
from app.infra.database.connection import Connection


class FileRepository(FileRepositoryContract):
    def __init__(self) -> None:
        self.db = Connection().get_database()

    def insert_one(self, file: File) -> File:

        file.id = str(uuid4())

        self.db.cursor().execute(
            "INSERT INTO file (id, fileName, orignalFilename, size) VALUES (?, ?, ?, ?)",
            (
                file.id,
                file.filename,
                file.orignalFilename,
                file.size,
            ),
        )

        self.db.commit()

        return file
