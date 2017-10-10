# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-10 12:56
from __future__ import unicode_literals

from django.db import migrations
import utf8field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dev_example', '0010_auto_20171010_1026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testcharfieldmodel',
            name='text',
        ),
        migrations.AddField(
            model_name='testcharfieldmodel',
            name='char',
            field=utf8field.fields.UTF8CharField(default='', four_byte_detection=True, max_length=2000),
            preserve_default=False,
        ),
    ]