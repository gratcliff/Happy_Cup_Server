# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-21 03:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0002_auto_20161121_0318'),
    ]

    operations = [
        migrations.AddField(
            model_name='cafe_content',
            name='description',
            field=models.TextField(default='Description for Happy Cup Coffee Cafe in Town Hall!'),
        ),
    ]
