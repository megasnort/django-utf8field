# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from utf8field.fields import UTF8FileField, UTF8CharField, UTF8TextField


class TestModel(models.Model):
    file = UTF8FileField(upload_to='media/')


class TestWithMaxContentLengthModel(models.Model):
    file = UTF8FileField(max_content_length=1000, upload_to='media/')


class TestCharFieldModel(models.Model):
    text = UTF8CharField(max_length=2000)


class TestTextFieldModel(models.Model):
    text = UTF8TextField()


class Message(models.Model):
    text = UTF8CharField(blank=True, null=True, max_length=2000)
    char = UTF8TextField(blank=True, null=True, max_length=2000)
    file = UTF8FileField(blank=True, null=True, max_length=2000)

