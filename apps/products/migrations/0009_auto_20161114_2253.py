# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 22:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20161114_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='wholesale_coffees',
            field=models.ManyToManyField(blank=True, to='products.WholeSaleCoffee'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='coffees',
            field=models.ManyToManyField(blank=True, to='products.Coffee'),
        ),
    ]
