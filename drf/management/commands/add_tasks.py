import json
from datetime import datetime, timedelta

from django_celery_beat.models import PeriodicTask, \
    IntervalSchedule

schedule, created = IntervalSchedule.objects.get_or_create(
     every=10,
     period=IntervalSchedule.SECONDS,
 )

PeriodicTask.objects.create(
     interval=schedule,
     name='Importing contacts',
     task='payment.tasks.payment_status_check',
     expires=datetime.utcnow() + timedelta(seconds=30)
 )