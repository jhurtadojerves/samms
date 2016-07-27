# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-27 00:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planificacion', '0007_auto_20160726_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tema',
            name='estado',
            field=models.CharField(blank=True, choices=[('0', 'Sin Revisar'), ('1', 'Aprobado'), ('2', 'No Aprobado')], default='0', max_length=1),
        ),
        migrations.AlterField(
            model_name='tema',
            name='fecha',
            field=models.DateField(blank=True),
        ),
    ]