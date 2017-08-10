# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from utf8field.fields import UTF8FileField


class TestModel(models.Model):
    file = UTF8FileField(upload_to='media/')
