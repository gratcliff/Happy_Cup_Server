# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 22:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about_page', '0002_auto_20161031_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fullwidthsection',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='fullwidthsection',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='staffmemberentry',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='staffmemberentry',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
