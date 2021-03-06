# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-11 23:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_auto_20161110_2013'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64)),
                ('email', models.EmailField(max_length=128)),
                ('phone_number', models.CharField(max_length=24)),
                ('address', models.TextField()),
                ('address2', models.TextField(blank=True)),
                ('city', models.CharField(max_length=32)),
                ('state', models.CharField(max_length=32)),
                ('zipcode', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Customer')),
            ],
        ),
    ]
