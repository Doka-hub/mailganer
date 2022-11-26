# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-11-25 12:18
from __future__ import unicode_literals

from django.db import migrations, models
import mailing.validators


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0005_auto_20221125_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='date_mail',
            field=models.DateTimeField(blank=True, null=True, validators=[mailing.validators.date_mail_validator], verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438'),
        ),
        migrations.AlterField(
            model_name='mail',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='mail', verbose_name='\u0424\u0430\u0439\u043b'),
        ),
    ]
