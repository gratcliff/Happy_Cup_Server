# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-15 01:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20161115_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='image_url',
            field=models.URLField(default='www.google.com'),
            preserve_default=False,
        ),
    ]
