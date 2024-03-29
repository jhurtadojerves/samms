# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-12 03:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estudiante', '0001_initial'),
        ('docenteAsignaturaPeriodo', '0001_initial'),
        ('horario', '0001_initial'),
        ('planificacion', '0002_auto_20160711_2246'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=256)),
                ('fecha', models.DateField()),
                ('estado', models.CharField(choices=[('0', 'Sin Revisar'), ('1', 'Aprobado'), ('2', 'No Aprobado')], default='0', max_length=1)),
                ('comentario', models.TextField(max_length=256, null=True)),
                ('aprobar_otra_fecha', models.BooleanField(default=False)),
                ('horario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horario.Horario')),
                ('revisado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='estudiante.Estudiante')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='planificacion',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='planificacion',
            name='revisado_por',
        ),
        migrations.RemoveField(
            model_name='planificacion',
            name='unidad',
        ),
        migrations.RemoveField(
            model_name='unidad',
            name='horario',
        ),
        migrations.AddField(
            model_name='unidad',
            name='asignatura',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='docenteAsignaturaPeriodo.DocenteAsignaturaPeriodo'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Planificacion',
        ),
        migrations.AddField(
            model_name='tema',
            name='unidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planificacion.Unidad'),
        ),
        migrations.AlterUniqueTogether(
            name='tema',
            unique_together=set([('unidad', 'fecha')]),
        ),
    ]
