from smtplib import SMTPException
from unittest.mock import MagicMock, create_autospec, patch

from pytest import fixture

from app.infra.logging.logging import Logging
from app.infra.mail.mail import SmtpMail


class FakeSMTP:
    def __init__(self, *params, **kprams) -> None:
        pass

    def login(self, *params):
        pass

    def sendmail(self, *params):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            raise exc_type


@fixture
def sut():
    return SmtpMail(create_autospec(Logging))


def test_get_generic_error_on_send_mail(sut: SmtpMail, faker):

    with patch("app.infra.mail.mail.smtplib.SMTP_SSL", new=FakeSMTP) as fake_smtp:
        fake_smtp.login = MagicMock(side_effect=Exception)
        fake_smtp.sendmail = MagicMock()
        result = sut.send_simple_mail([faker.email()], faker.word(), faker.word())

    assert result is False
    fake_smtp.login.assert_called_once()
    fake_smtp.sendmail.assert_not_called()

def test_get_smtp_exception_error_on_send_mail(sut: SmtpMail, faker):

    with patch("app.infra.mail.mail.smtplib.SMTP_SSL", new=FakeSMTP) as fake_smtp:
        fake_smtp.login = MagicMock(side_effect=SMTPException)
        fake_smtp.sendmail = MagicMock()
        result = sut.send_simple_mail([faker.email()], faker.word(), faker.word())

    assert result is False
    fake_smtp.login.assert_called_once()
    fake_smtp.sendmail.assert_not_called()

def test_should_execute_with_success(sut: SmtpMail, faker):

    with patch("app.infra.mail.mail.smtplib.SMTP_SSL", new=FakeSMTP) as fake_smtp:
        fake_smtp.login = MagicMock()
        fake_smtp.sendmail = MagicMock()
        result = sut.send_simple_mail([faker.email()], faker.word(), faker.word())

    assert result is True
    fake_smtp.login.assert_called_once()
    fake_smtp.sendmail.assert_called_once()
