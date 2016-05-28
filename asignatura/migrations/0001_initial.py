# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-28 03:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carrera', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=32, unique=True)),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('nivel', models.CharField(blank=True, max_length=16, null=True)),
                ('horas', models.IntegerField()),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carrera.Carrera')),
            ],
        ),
    ]
