# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-03-18 03:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0005_auto_20190318_0327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dormitory',
            name='staff',
        ),
    ]
