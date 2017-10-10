# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.edit import CreateView

from rest_framework import generics

from .models import TestModel, TestWithMaxContentLengthModel, TestCharFieldModel, \
    TestTextFieldModel, Message, PermissiveMessage
from .serializers import MessageSerializer


class MessageViews(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class TestCreate(CreateView):
    template_name = 'dev_example/test_view.html'
    model = TestModel
    success_url = '/'
    fields = ['file', ]


class TestMaxContentLengthCreate(CreateView):
    template_name = 'dev_example/test_view.html'
    model = TestWithMaxContentLengthModel
    success_url = '/max-content-length/'
    fields = ['file', ]


class TestCreateCharField(CreateView):
    template_name = 'dev_example/test_view.html'
    model = TestCharFieldModel
    success_url = '/char-field/'
    fields = ['char', ]


class TestCreateTextField(CreateView):
    template_name = 'dev_example/test_view.html'
    model = TestTextFieldModel
    success_url = '/text-field/'
    fields = ['text', ]


class PermissiveMessageCreate(CreateView):
    template_name = 'dev_example/test_view.html'
    model = PermissiveMessage
    success_url = '/permissive-message'
    fields = ['file', 'text', 'char', ]
