import os

from app.infra.database.connection import Connection


class MigrationRunner:

    def _open_connection(self):
        pass

    def _load_files_path(self):
        return os.path.dirname(__file__) + "/../../../../sql/"

    def _load_files(self):

        path = self._load_files_path()

        sql_files = [
            filename
            for filename in os.listdir(path)
            if os.path.isfile(f"{path}{filename}")
            and filename.endswith(".sql")
            and "manual" not in filename
        ]

        return sql_files

    def _load_file(self, filename: str) -> str:
        with open(f"{self._load_files_path()}{filename}", "r") as sql_file:
            return sql_file.read()

    def execute(self):
        files = self._load_files()
        conn = Connection()

        db = conn.get_database()

        for sql in files:
            was_executed = db.execute(
                "select * from migrations where fileName = (?);", (sql,)
            ).fetchone()

            if not was_executed:
                print(f"executing {sql} ...")
                db.executescript(self._load_file(sql))
                db.execute("INSERT INTO migrations (fileName) values (?)", (sql,))
                db.commit()
                print("executed ...")

        db.close()


if __name__ == "__main__":
    m = MigrationRunner()
    m.execute()
    print("all done :)")
