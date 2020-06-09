from __future__ import absolute_import
from kombu import Exchange, Queue
from celery.schedules import crontab

result_backend = 'redis://127.0.0.1:6379/5'
broker_url = 'redis://127.0.0.1:6379/6'

# task_queues = (
#     Queue('default', Exchange('default', type='direct'), routing_key='default'),
#     Queue('for_task_a', Exchange('for_task_a', type='direct'), routing_key='task_a'),
#     Queue('for_task_b', Exchange('for_task_b', type='direct'), routing_key='task_b')
# )
#
# task_routes = {
#     'tasks.taskA': {"queue": "for_task_A", "routing_key": "task_a"},
#     'tasks.taskB': {"queue": "for_task_B", "routing_key": "task_b"}
# }

timezone = 'Asia/Shanghai'

from datetime import timedelta

# beat_schedule = {
#     'taskA_schedule' : {
#         'task':'tasks.taskA',
#         'schedule':20,
#         'args':(5,6)
#     },
#     'taskB_scheduler' : {
#         'task':"tasks.taskB",
#         "schedule":200,
#         "args":(10,20,30)
#     },
#     'add_schedule': {
#         "task":"tasks.add",
#         "schedule":10,
#         "args":(1,2)
#     },
# # Executes every Monday morning at 7:30 A.M
#     'add-every-monday-morning': {
#         'task': 'tasks.add',
#         'schedule': crontab(hour=7, minute=30, day_of_week=1),
#         'args': (16, 16),
#     },
#
# }
