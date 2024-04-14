class FakeDB:
    def cursor(self):
        return self

    def commit(self):
        return self

    def execute(self, *params):
        return self
