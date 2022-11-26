from __future__ import absolute_import

from celery import Celery

import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')


celery_app = Celery('app', result_expires=60)
celery_app.config_from_object('django.conf:settings')

celery_app.autodiscover_tasks()
