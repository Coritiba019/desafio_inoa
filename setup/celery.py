# celery.py
from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

app = Celery('setup')
app.conf.update(timezone='America/Sao_Paulo')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
