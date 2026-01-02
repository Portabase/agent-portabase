import os
import sys
import warnings
from celery import Celery
from kombu import Exchange, Queue
from logging_config import setup_logging
from settings import config
from celery.schedules import crontab
from tasks.ping import ping_server
from utils.init import initialize_directories


def create_celery_app():
    app = Celery('portabase-agent')

    app.conf.broker_url = config.CELERY_BROKER_URL
    app.conf.result_backend = config.CELERY_RESULT_BACKEND
    app.conf.broker_connection_retry_on_startup = True

    default_exchange = Exchange('default', type='topic')

    app.conf.task_queues = (
        Queue('default', default_exchange, routing_key='default.#'),
        Queue('periodic', default_exchange, routing_key='periodic.#'),
    )

    app.conf.task_default_queue = 'default'
    app.conf.task_default_exchange = 'default'
    app.conf.task_default_routing_key = 'default'

    app.autodiscover_tasks()


    ping_crontab = crontab(
        minute='*',
        hour='*',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
    )

    app.add_periodic_task(
        ping_crontab,
        ping_server,
        name="periodic.ping_server",
        bind=True,
    )

    return app


def run_initialization():
    if not initialize_directories():
        sys.exit(1)

    warnings.filterwarnings("ignore", category=UserWarning)

    if os.getenv("ENVIRONMENT") != "development":
        setup_logging()

    return create_celery_app()


app = run_initialization()
