# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 22:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20161107_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerorder',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='customerorder',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]