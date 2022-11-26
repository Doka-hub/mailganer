# coding: utf-8
from __future__ import unicode_literals

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from app.celery import celery_app

from .models import Mail


@celery_app.task(name='send_mail')
def send_mail(mail_id):
    mail = Mail.objects.get(id=mail_id)
    subscribers = mail.get_subscribers()
    for subscriber in subscribers:
        text = mail.get_formatted_text(subscriber)
        msg = EmailMultiAlternatives(
            subject=mail.title,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.email]
        )
        msg.attach_alternative(text, 'text/html')
        msg.send()
