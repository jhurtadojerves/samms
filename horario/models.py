# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from docenteAsignaturaNivelPeriodo.models import DocenteAsignaturaNivelPeriodo

# Create your models here.

class Horario(models.Model):
    asignatura = models.ForeignKey(DocenteAsignaturaNivelPeriodo)
    dias = (
        ('0', 'Lunes'),
        ('1', 'Martes'),
        ('2', 'Miercoles'),
        ('3', 'Jueves'),
        ('4', 'Viernes')
    )
    dia = models.CharField(max_length=1, choices=dias, default='0')
    inicio = models.TimeField()
    fin = models.TimeField()