# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-08 14:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20171208_1435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metering',
            name='is_test',
        ),
        migrations.RemoveField(
            model_name='station',
            name='is_in_test_mode',
        ),
    ]
