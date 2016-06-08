# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 00:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictado', '0003_dictado_revisado_por'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictado',
            name='tema',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='dictado',
            unique_together=set([('horario', 'fecha')]),
        ),
    ]
