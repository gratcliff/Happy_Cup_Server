# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-21 21:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20161118_1732'),
        ('customers', '0015_auto_20161119_0016'),
        ('orders', '0008_auto_20161119_0016'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(max_length=40)),
                ('coffee', models.TextField(max_length=24)),
                ('grind', models.CharField(max_length=24)),
                ('size', models.CharField(max_length=8)),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('status', models.CharField(default='active', max_length=40)),
                ('shipping_address', models.TextField(blank=True)),
                ('shipping_fee', models.PositiveSmallIntegerField(default=0)),
                ('subTotalPrice', models.FloatField(default=0, verbose_name='Price before shipping')),
                ('totalPrice', models.FloatField(verbose_name='Total Price')),
                ('other_info', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Customer')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Subscription')),
            ],
        ),
    ]
