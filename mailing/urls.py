from django.conf.urls import url

from .views import (
    HeadTemplateView,

    ListCreateView,
    ListListView,

    SubscribersCreateView,
    SubscribersListView,

    MailCreateView,
    MailListView,
)


app_name = 'mailing'

urlpatterns = [
    url(r'^$', HeadTemplateView.as_view(), name='head'),

    url(r'^list/create/', ListCreateView.as_view(), name='list-create'),
    url(r'^list/list/', ListListView.as_view(), name='list-list'),

    url(r'^subscribers/create/', SubscribersCreateView.as_view(), name='subscribers-create'),
    url(r'^subscribers/list/', SubscribersListView.as_view(), name='subscribers-list'),

    url(r'^mail/create/', MailCreateView.as_view(), name='mail-create'),
    url(r'^mail/list/', MailListView.as_view(), name='mail-list'),
]
