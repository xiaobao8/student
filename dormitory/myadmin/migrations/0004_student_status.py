# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-03-17 23:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0003_auto_20190317_0514'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='status',
            field=models.BooleanField(default=1),
        ),
    ]
