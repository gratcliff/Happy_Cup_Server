# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-08 23:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_wholesalecoffee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wholesalecoffee',
            name='size',
        ),
    ]
