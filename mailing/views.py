# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
)

from .models import List, Subscriber, Mail
from .forms import (
    ListCreateForm,
    SubscriberCreateForm,
    MailCreateForm,
)


class HeadTemplateView(TemplateView, LoginRequiredMixin):
    template_name = 'mailing/head.html'


class ListCreateView(CreateView, LoginRequiredMixin):
    template_name = 'mailing/list-create.html'

    model = List
    form_class = ListCreateForm

    success_url = reverse_lazy('mailing:list-list')

    def get_form_kwargs(self):
        kwargs = super(ListCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ListListView(ListView, LoginRequiredMixin):
    template_name = 'mailing/list-list.html'

    model = List
    context_object_name = 'list_list'

    def get_queryset(self):
        queryset = self.model.objects.filter(owner=self.request.user)
        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(*ordering)
        return queryset


class SubscribersCreateView(CreateView, LoginRequiredMixin):
    template_name = 'mailing/subscriber-create.html'

    model = Subscriber
    form_class = SubscriberCreateForm

    success_url = reverse_lazy('mailing:subscribers-list')

    def get_form_kwargs(self):
        kwargs = super(SubscribersCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class SubscribersListView(ListView, LoginRequiredMixin):
    template_name = 'mailing/subscriber-list.html'
    
    model = Subscriber
    context_object_name = 'subscriber_list'

    def get_queryset(self):
        queryset = self.model.objects.filter(list__owner=self.request.user)
        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(*ordering)
        return queryset


class MailCreateView(CreateView, LoginRequiredMixin):
    template_name = 'mailing/mail-create.html'

    model = Mail
    form_class = MailCreateForm

    success_url = reverse_lazy('mailing:mail-list')

    def get_form_kwargs(self):
        kwargs = super(MailCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailListView(LoginRequiredMixin, ListView):
    template_name = 'mailing/mail-list.html'

    model = Mail
    context_object_name = 'mail_list'

    def get_queryset(self):
        queryset = self.model.objects.filter(list__owner=self.request.user)
        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(*ordering)
        return queryset
