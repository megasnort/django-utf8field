# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-11 06:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dev_example', '0003_testcharfieldmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testcharfieldmodel',
            old_name='file',
            new_name='text',
        ),
    ]
