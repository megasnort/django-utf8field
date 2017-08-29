# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from utf8field.fields import UTF8FileField


class TestModel(models.Model):
    file = UTF8FileField(upload_to='media/')


class TestWithMaxContentLengthModel(models.Model):
    file = UTF8FileField(max_content_length=1000, upload_to='media/')
