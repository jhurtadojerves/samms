# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-01 22:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('horario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horario',
            name='asignatura',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='docenteAsignaturaPeriodo.DocenteAsignaturaPeriodo'),
        ),
    ]
