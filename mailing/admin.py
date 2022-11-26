# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import List, Subscriber, Mail


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    pass


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('id', 'list', 'sender_email', 'date_mail', 'created')
