# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User

import csv

from .validators import mail_text_validator, date_mail_validator


class List(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='lists', blank=True,
                              verbose_name='Владелец')
    name = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = 'Список'
        verbose_name_plural = 'Списки'

    def __unicode__(self):
        return '%s: %s' % (self.owner, self.name)


class Subscriber(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE,
                             related_name='subscribers',
                             verbose_name='Список')
    email = models.EmailField(blank=True, verbose_name='Email')
    name = models.CharField(max_length=255, blank=True, verbose_name='Имя')
    surname = models.CharField(max_length=255, blank=True,
                               verbose_name='Фамилия')
    birthday = models.CharField(max_length=255, blank=True,
                                verbose_name='День рождение')
    age = models.IntegerField(blank=True, null=True, verbose_name='Возраст')
    phone = models.CharField(max_length=255, blank=True,
                             verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    def __unicode__(self):
        return '%s - %s - %s' % (self.list, self.email, self.name)

    @classmethod
    def create_from_csv(cls, list_, file_):
        data = csv.reader(file_, delimiter=str(';'))
        fields_names = list(map(lambda x: x.lower(), data.next()))

        subscriber_list = []
        for field_list in data:
            if field_list:
                obj_data = {}
                for index_, field in enumerate(field_list):
                    obj_data[fields_names[index_]] = field
                try:
                    obj = cls.objects.get(list=list_, email=obj_data['email'])

                    for i in obj_data:
                        setattr(obj, i, obj_data[i])
                    obj.save(update_fields=obj_data.keys())
                except cls.DoesNotExist:
                    obj = cls(list=list_, **obj_data)
                    subscriber_list.append(obj)
        print subscriber_list
        cls.objects.bulk_create(subscriber_list)


class Mail(models.Model):
    FORMATS = (
        ('{{name}}', 'name'),
        ('{{surname}}', 'surname'),
        ('{{email}}', 'email'),
        ('{{birthday}}', 'birthday'),
        ('{{age}}', 'age'),
        ('{{phone}}', 'phone'),
    )

    list = models.ForeignKey(List, on_delete=models.CASCADE,
                             related_name='mails', verbose_name='Список')
    sender_email = models.CharField(max_length=255,
                                    verbose_name='Почта отправителя')

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(validators=[mail_text_validator],
                            verbose_name='Текст')
    file = models.FileField(blank=True, null=True, upload_to='mail',
                            verbose_name='Файл')

    date_mail = models.DateTimeField(blank=True, null=True,
                                     validators=[date_mail_validator],
                                     verbose_name='Дата отправки')
    send = models.BooleanField(default=True, verbose_name='Отправить')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __unicode__(self):
        return '%s - %s - %s' % (self.list, self.sender_email, self.date_mail)

    def get_subscribers(self):
        return self.list.subscribers.all()

    def get_formatted_text(self, subscriber):
        for format_ in self.FORMATS:
            self.text = self.text.replace(
                format_[0],
                str(getattr(subscriber, format_[1])),
            )
        return self.text


@receiver(post_save, sender=Mail)
def mail(sender, created, instance, **kwargs):
    if instance.send:
        from .tasks import send_mail

        if not instance.date_mail:
            send_mail.delay(instance.id)
        else:
            send_mail.apply_async(
                (instance.id,),
                eta=instance.date_mail,
            )
        instance.send = False
        instance.save(update_fields=['send'])
