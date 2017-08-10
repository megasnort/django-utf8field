# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .forms import TestForm


def test_view(request):
    form = TestForm()

    return render(
        request,
        'dev_example/test_view.html',
        {
            'form': form
        }
    )

