# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.utils import timezone


def mail_text_validator(value):
    if '<a href="{{unsubscribeUrl}}">' not in value:
        raise ValidationError(
            'Отсутствует ссылка отписки. Используйте переменную {{unsubscribeUrl}} в рассылке. Например, <a href="{{unsubscribeUrl}}">ссылка отписки</a>'
        )


def date_mail_validator(value):
    if timezone.now() > value.astimezone(timezone.utc):
        raise ValidationError(
            'Дата отправки должна быть в будущем'
        )
