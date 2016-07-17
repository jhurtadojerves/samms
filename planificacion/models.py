# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms

from horario.models import Horario
from estudiante.models import Estudiante
from docenteAsignaturaPeriodo.models import DocenteAsignaturaPeriodo

# Create your models here.

class Unidad(models.Model):
    nombre = models.CharField(max_length=256, null=False)
    asignatura = models.ForeignKey(DocenteAsignaturaPeriodo)

    def __unicode__(self):
        return self.nombre

class Tema(models.Model):
    descripcion = models.CharField(max_length=256, null=False)
    unidad = models.ForeignKey(Unidad, blank = True)
    horario = models.ForeignKey(Horario, blank = True)
    fecha = models.DateField(null=False)
    estado_opciones = (
        ('0', 'Sin Revisar'),
        ('1', 'Aprobado'),
        ('2', 'No Aprobado')
    )
    estado = models.CharField(max_length=1, choices=estado_opciones, default='0')
    revisado_por = models.ForeignKey(Estudiante, null=True, blank=True)
    comentario = models.TextField(max_length=256, null=True, blank = True)
    aprobar_otra_fecha = models.BooleanField(default=False)

    def tema_string(self):
        return dict(Tema.estado_opciones)[self.estado]

    def clean(self):
        try:
            if ((int(self.horario.dia )!= int(self.fecha.weekday()))):
                raise forms.ValidationError('El día y la fecha no coinciden')
            else:
                return self
        except:
            return self
            #raise forms.ValidationError('Horario no definido')
    class Meta:
        unique_together = ('unidad', 'fecha',)