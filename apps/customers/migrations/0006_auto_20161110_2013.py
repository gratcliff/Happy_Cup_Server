# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 20:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_auto_20161107_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=24),
        ),
    ]
