# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-10 17:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('docenteAsignaturaPeriodoEstudiante', '0001_initial'),
        ('estudiante', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='docenteasignaturaperiodoestudiante',
            name='estudiante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estudiante.Estudiante'),
        ),
    ]
