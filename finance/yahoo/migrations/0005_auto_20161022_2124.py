# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-22 21:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yahoo', '0004_auto_20161022_2124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='price',
        ),
        migrations.AlterField(
            model_name='stock',
            name='shares',
            field=models.IntegerField(),
        ),
    ]
