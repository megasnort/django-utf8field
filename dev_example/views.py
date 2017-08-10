# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.edit import CreateView

from .models import TestModel


class TestCreate(CreateView):
    template_name = 'dev_example/test_view.html'
    model = TestModel
    success_url = '/'
    fields = ['file', ]
