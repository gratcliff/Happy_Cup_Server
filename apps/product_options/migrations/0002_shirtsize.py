# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 20:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_options', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShirtSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('size', models.CharField(choices=[('XS', 'X-Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'X-Large'), ('2XL', '2X-Large'), ('3XL', '3X-Large')], max_length=3, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
