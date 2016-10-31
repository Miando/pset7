# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yahoo', '0009_auto_20161026_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='symbol',
            field=models.CharField(max_length=10, verbose_name='symbol'),
        ),
    ]
