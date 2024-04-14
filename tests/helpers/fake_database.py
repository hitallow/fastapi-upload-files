class FakeDB:
    def cursor(self):
        return self

    def commit(self):
        return self

    def fetchone(self):
        return self
    
    def fetchall(self):
        return self

    def execute(self, *params):
        return self
    
    def executemany(self, *params):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *params):
        pass
