# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-07 14:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('horario', '0006_horario_activo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='horario',
            name='activo',
        ),
    ]
