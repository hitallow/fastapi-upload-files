import schedule

from app.presentation.factories.init_notify_boletos_factory import \
    init_notify_boletos_factory


def notify_users():
    init_notify_boletos_factory().execute(None)


def register():
    # schedule.every(60).seconds.do(notify_users) for tests
    schedule.every().day.at("02:00").do(notify_users)  # for prod
