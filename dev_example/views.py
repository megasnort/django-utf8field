# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.edit import CreateView

from .models import TestModel, TestWithMaxContentLengthModel


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
