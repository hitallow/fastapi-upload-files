from pytest import fixture

from tests.helpers.fake_database import FakeDB


@fixture
def fake_database():
    return FakeDB()