# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-15 00:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20161114_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='stripe_id',
            field=models.CharField(blank=True, help_text='Ignore this field. Data is be added after plan is created.', max_length=32),
        ),
    ]
