# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-07 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horario', '0005_auto_20160801_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='horario',
            name='activo',
            field=models.BooleanField(default=False),
        ),
    ]
