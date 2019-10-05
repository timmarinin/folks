from celery import Celery

from celery.utils.log import get_task_logger

from config import Config
logger = get_task_logger(__name__)
app = Celery('folks', broker=Config.CELERY_BROKER, include=['tasks.images', 'tasks.feeds'])
app.conf.result_backend = Config.CELERY_BROKER