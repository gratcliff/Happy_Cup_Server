# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 21:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_subscription_image_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wholesalecoffee',
            options={'verbose_name': 'Coffees - Wholesale'},
        ),
    ]