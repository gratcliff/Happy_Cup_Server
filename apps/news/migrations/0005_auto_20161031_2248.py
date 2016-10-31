# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 22:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_blogpost_old_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='old_created_at',
            field=models.DateField(blank=True, help_text='Leave field blank if this is a new post.', null=True, verbose_name='Date of previous publication'),
        ),
    ]