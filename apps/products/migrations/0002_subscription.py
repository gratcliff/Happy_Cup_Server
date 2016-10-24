# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('frequency', models.PositiveSmallIntegerField(verbose_name='Number of weeks between each shipment')),
                ('coffees', models.ManyToManyField(to='products.Coffee')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]