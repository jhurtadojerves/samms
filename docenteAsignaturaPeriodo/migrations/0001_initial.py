# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 23:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('asignatura', '0001_initial'),
        ('docente', '0001_initial'),
        ('periodo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocenteAsignaturaPeriodo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asignatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asignatura.Asignatura')),
                ('docente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docente.Docente')),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='periodo.Periodo')),
            ],
        ),
    ]