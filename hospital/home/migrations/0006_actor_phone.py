# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-30 17:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20190330_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='phone',
            field=models.CharField(default=1, max_length=11, unique=True),
            preserve_default=False,
        ),
    ]