# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.edit import CreateView

from .models import TestModel, TestWithMaxContentLengthModel, TestCharFieldModel, TestTextFieldModel


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
    fields = ['text', ]


class TestCreateTextField(CreateView):
    template_name = 'dev_example/test_view.html'
    model = TestTextFieldModel
    success_url = '/text-field/'
    fields = ['text', ]