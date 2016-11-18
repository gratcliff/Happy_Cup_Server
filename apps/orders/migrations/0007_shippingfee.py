# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-17 01:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_customerorder_shipping_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingFee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_weight', models.SmallIntegerField(help_text='Pounds', unique=True, verbose_name='Minimum weight in range')),
                ('max_weight', models.SmallIntegerField(help_text='Pounds', unique=True, verbose_name='Maximum weight in range')),
                ('price', models.SmallIntegerField(help_text='Whole Dollars')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['price'],
            },
        ),
    ]