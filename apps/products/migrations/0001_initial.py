# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 16:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product_options', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coffee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=24)),
                ('description', models.TextField()),
                ('image_url', models.URLField()),
                ('price_factor', models.SmallIntegerField(default=0, verbose_name='Increase or decrease the base price by the following percentage.  Use negative values to decrease price.')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Merchandise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=24)),
                ('description', models.TextField()),
                ('image_url', models.URLField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'verbose_name_plural': 'Merchandise',
            },
        ),
        migrations.CreateModel(
            name='ProductPromotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=64)),
                ('discount', models.PositiveSmallIntegerField(default=15, help_text='Positive, whole numbers only', verbose_name='Percent discount')),
                ('expiration_date', models.DateTimeField(verbose_name='Date and time that promotion ends')),
                ('expired', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('frequency', models.PositiveSmallIntegerField(verbose_name='Number of weeks between each shipment')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('coffees', models.ManyToManyField(to='products.Coffee')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VarietyPack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=24)),
                ('description', models.TextField()),
                ('image_url', models.URLField()),
                ('coffee_qty', models.PositiveSmallIntegerField(default=0, verbose_name='Number of bags of coffee in variety pack (if applicable)')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('coffees', models.ManyToManyField(blank=True, to='products.Coffee', verbose_name='Coffees in variety pack (if applicable)')),
                ('featured', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.ProductPromotion', verbose_name='To feature this product, select a promotional deal.')),
                ('merchandise', models.ManyToManyField(blank=True, to='products.Merchandise', verbose_name='Merchandise in variety pack (if applicable)')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='merchandise',
            name='featured',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.ProductPromotion', verbose_name='To feature this product, select a promotional deal.'),
        ),
        migrations.AddField(
            model_name='merchandise',
            name='sizes',
            field=models.ManyToManyField(blank=True, to='product_options.ShirtSize', verbose_name='Shirt Sizes available (if applicable)'),
        ),
        migrations.AddField(
            model_name='coffee',
            name='featured',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.ProductPromotion', verbose_name='To feature this product, select a promotional deal.'),
        ),
        migrations.AddField(
            model_name='coffee',
            name='grinds',
            field=models.ManyToManyField(to='product_options.CoffeeGrind'),
        ),
        migrations.AddField(
            model_name='coffee',
            name='roast',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_options.CoffeeRoast'),
        ),
        migrations.AddField(
            model_name='coffee',
            name='sizes',
            field=models.ManyToManyField(to='product_options.CoffeeVolume'),
        ),
    ]
