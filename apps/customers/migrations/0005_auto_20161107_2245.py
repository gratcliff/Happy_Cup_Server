# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 22:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_auto_20161107_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]