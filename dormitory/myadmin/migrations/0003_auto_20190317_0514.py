# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-03-17 05:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0002_auto_20190317_0351'),
    ]

    operations = [
        migrations.AddField(
            model_name='dormitory',
            name='storied',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myadmin.Storied'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dormitory',
            name='number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='storied',
            name='number',
            field=models.IntegerField(unique=True),
        ),
    ]
