# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 17:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictado', '0005_auto_20160606_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictado',
            name='comentario',
            field=models.TextField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dictado',
            name='tema',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name='dictado',
            name='unidad',
            field=models.TextField(max_length=255),
        ),
    ]
