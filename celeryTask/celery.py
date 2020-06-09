from __future__ import absolute_import
from celery import Celery

app = Celery('celeryTask', include=['celeryTask.tasks'])

app.config_from_object('celeryTask.celeryConfig')

if __name__ == '__main__':
    app.start()