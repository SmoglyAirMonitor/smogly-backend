# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-08 15:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20171208_1438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metering',
            name='hw_id',
        ),
    ]
