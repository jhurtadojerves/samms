# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-05 00:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('horario', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='horario',
            unique_together=set([('asignatura', 'dia')]),
        ),
    ]
