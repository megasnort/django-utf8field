# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from utf8field.fields import UTF8FileField, UTF8CharField, UTF8TextField


class TestModel(models.Model):
    file = UTF8FileField(upload_to='media/', four_byte_detection=True)


class TestWithMaxContentLengthModel(models.Model):
    file = UTF8FileField(max_content_length=1000, four_byte_detection=True, upload_to='media/')


class TestCharFieldModel(models.Model):
    char = UTF8CharField(max_length=2000, four_byte_detection=True)


class TestTextFieldModel(models.Model):
    text = UTF8TextField(four_byte_detection=True)


class Message(models.Model):
    text = UTF8TextField(blank=True, null=True)
    char = UTF8CharField(max_length=2000, blank=True, null=True)
    file = UTF8FileField(blank=True, null=True, max_length=2000, four_byte_detection=True)


class PermissiveMessage(models.Model):
    text = UTF8TextField(blank=True, null=True)
    char = UTF8CharField(max_length=2000, blank=True, null=True)
    file = UTF8FileField(blank=True, null=True, four_byte_detection=False)
