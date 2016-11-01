# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-01 23:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=24)),
                ('address_1', models.TextField()),
                ('address_2', models.TextField(blank=True)),
                ('city', models.CharField(max_length=32)),
                ('state', models.CharField(max_length=24)),
                ('zip_code', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='DiscountRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_percentage', models.PositiveSmallIntegerField(help_text='Percentage discount customer will receive on all coffee orders.')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='discount_rate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customers.DiscountRate'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
