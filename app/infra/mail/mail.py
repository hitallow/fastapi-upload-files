import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from app.domain.contracts.logging import Logging
from app.domain.contracts.mail import Mail


class SmtpMail(Mail):

    def __init__(self, logging: Logging) -> None:
        self.logging = logging

    def send_simple_mail(self, to: List[str], subject: str, message: str) -> bool:
        try:
            msg = MIMEMultipart()
            msg["From"] = os.getenv("MAIL_FROM")
            msg["To"] = ", ".join(to)
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))

            with smtplib.SMTP_SSL(os.getenv("MAIL_HOST"), int(os.getenv("MAIL_PORT") or 465), timeout=30) as smtp: # type: ignore
                smtp.login(os.getenv("MAIL_FROM"), os.getenv("MAIL_PASSWORD"))  # type: ignore
                smtp.sendmail(os.getenv("MAIL_USERNAME"), to, msg.as_string())  # type: ignore

            self.logging.info("sent with success")
            return True
        except smtplib.SMTPException as e:
            self.logging.info("error on sent email")
            self.logging.info(e)
            return False
        except Exception as e:
            self.logging.info("generic error on sent email")
            self.logging.info(e)
            return False
