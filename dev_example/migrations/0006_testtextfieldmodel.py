# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-11 09:07
from __future__ import unicode_literals

from django.db import migrations, models
import utf8field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dev_example', '0005_auto_20170911_0658'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestTextFieldModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', utf8field.fields.UTF8TextField()),
            ],
        ),
    ]
