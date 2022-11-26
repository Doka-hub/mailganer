# -*- coding: utf-8 -*-
from django import forms

from .models import List, Subscriber, Mail


class ListCreateForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ('owner', 'name',)
        widgets = {
            'owner': forms.HiddenInput(),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ListCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.owner = self.user
        return super(ListCreateForm, self).save(commit)


class SubscriberCreateForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = Subscriber
        fields = ('list', 'file')
        widgets = {
            'list': forms.Select(attrs={
                'class': 'form-control',
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SubscriberCreateForm, self).__init__(*args, **kwargs)
        self.fields['list'].queryset = List.objects.filter(owner=user)

    def save(self, commit=True):
        self._meta.model.create_from_csv(
            self.cleaned_data['list'],
            self.cleaned_data['file'].file,
        )
        return self.instance


class MailCreateForm(forms.ModelForm):
    date_mail = forms.DateTimeField(
        ['%Y-%m-%dT%H:%M'],
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
        }),
    )

    class Meta:
        model = Mail
        fields = (
            'list',
            'title',
            'text',
            'file',
            'date_mail',
        )
        widgets = {
            'list': forms.Select(attrs={
                'class': 'form-control',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MailCreateForm, self).__init__(*args, **kwargs)
        self.fields['list'].queryset = List.objects.filter(owner=user)
