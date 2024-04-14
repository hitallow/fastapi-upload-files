from datetime import datetime
from time import time
from typing import List, Tuple
from uuid import uuid4

from app.domain.contracts import FileImportRepositoryContract
from app.domain.entities import FileImport
from app.domain.entities.paginted_list import PaginatedEntities
from app.domain.exceptions.entity_not_found_exception import \
    EntityNotFoundException
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

        if not reply:
            raise EntityNotFoundException("FileImport not found")

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

    def __count_all_items(self) -> int:
        return self.db.execute("select count(*) as total from fileImport;").fetchone()[0]

    def get_all(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> PaginatedEntities[FileImport]:

        sql = "SELECT id, title, status, createdAt, updatedAt FROM fileImport"


        if limit is not None and offset is not None:
            sql = f"{sql} LIMIT {limit} OFFSET {offset * limit}"

        file_imports = [
            FileImport(
                id=db_data[0],
                title=db_data[1],
                status=db_data[2],
                created_at=int(
                    datetime.strptime(db_data[3], "%Y-%m-%d %H:%M:%S").timestamp()
                ),
                updated_at=int(
                    datetime.strptime(db_data[4], "%Y-%m-%d %H:%M:%S").timestamp()
                ),
            )
            for db_data in self.db.execute(sql).fetchall()
        ]
        return PaginatedEntities(total_items=self.__count_all_items(), items=file_imports)
