from celery import shared_task
from django.core.mail import send_mail
import requests
from config import settings
from drf.models import Course, Subscribe, Payment, PaymentLog
from datetime import datetime, timedelta
import pytz
import hashlib


@shared_task
def subscribed_message(course_pk):
    subscribers = Subscribe.objects.filter(course=course_pk)
    course = Course.objects.filter(pk=course_pk).first()
    time = datetime.now().astimezone(pytz.timezone(settings.TIME_ZONE)) - timedelta(hours=4)

    if time >= course.time_update:

        for student in subscribers:
            send_mail(subject='Обновления курса',
                      message=f'Смотрите обновления курса "{course.course_title}" по ссылке {settings.BASE_URL}course/{course_pk}',
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[student.student.email],
                      fail_silently=False)

    course.time_update = datetime.now().astimezone(pytz.timezone(settings.TIME_ZONE))
    course.save()


def payment_status_check():
    payment_list = PaymentLog.objects.all()
    SSH_DICT = {}
    for item in payment_list:
        SSH = f'{settings.TERMINAL_PASSWORD}{item.PaymentId}{item.TerminalKey}'
        data_for_request = {
            "TerminalKey": settings.TERMINAL_KEY,
            "PaymentId": item.PaymentId,
            "Token": hashlib.sha256(SSH.encode()).hexdigest(),
        }
        response = requests.post('https://securepay.tinkoff.ru/v2/GetState', json=data_for_request)
        SSH_DICT[item.id] = f"{response.json()['Success']}"

    for k, v in SSH_DICT.items():
        print(f'PaymentId: {k}, Success: {v}')