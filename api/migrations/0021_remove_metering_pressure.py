# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-08 15:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_remove_metering_hw_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metering',
            name='pressure',
        ),
    ]
