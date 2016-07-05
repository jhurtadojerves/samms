# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date
from django import forms

from docenteAsignaturaPeriodo.models import DocenteAsignaturaPeriodo



# Create your models here.

class Horario(models.Model):
    asignatura = models.ForeignKey(DocenteAsignaturaPeriodo)
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

    def __unicode__(self):
        a = {0: 'Lunes', 1:'Martes', 2:'Miércoles', 3:'Jueves', 4: 'Viernes'}
        return self.asignatura.asignatura.descripcion + ' - ' + a[int(self.dia)]

    class Meta:
        unique_together = ('asignatura', 'dia',)

    def clean(self):
        if not self.fin>self.inicio:
            raise forms.ValidationError("La hora de fin debe ser posterior a la de inicio")
        else:
            return self