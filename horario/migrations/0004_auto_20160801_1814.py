# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-01 23:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horario', '0003_auto_20160801_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horario',
            name='fin',
            field=models.CharField(choices=[('1', '07:30'), ('2', '08:30'), ('3', '09:30'), ('4', '10:30'), ('5', '11:30'), ('6', '12:30'), ('7', '13:30'), ('8', '14:30'), ('9', '15:30'), ('10', '16:30')], default='09:30', max_length=5),
        ),
        migrations.AlterField(
            model_name='horario',
            name='inicio',
            field=models.CharField(choices=[('1', '07:30'), ('2', '08:30'), ('3', '09:30'), ('4', '10:30'), ('5', '11:30'), ('6', '12:30'), ('7', '13:30'), ('8', '14:30'), ('9', '15:30'), ('10', '16:30')], default='07:30', max_length=5),
        ),
    ]