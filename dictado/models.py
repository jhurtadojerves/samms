# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
from horario.models import Horario
from estudiante.models import Estudiante

# Create your models here.

class Dictado(models.Model):
    horario = models.ForeignKey(Horario)
    unidad = models.TextField(max_length=255, null=False, blank=False)
    tema = models.TextField(max_length=255, null=False, blank=False)
    fecha = models.DateField(auto_now_add=True)
    estado_opciones = (
        ('0', 'Sin Revisar'),
        ('1', 'Aprobado'),
        ('2', 'No Aprobado')
    )
    estado = models.CharField(max_length=1, choices=estado_opciones, default='0')
    revisado_por = models.ForeignKey(Estudiante, null=True)
    comentario = models.TextField(max_length=255, null=True)

    def clean(self):
        try:
            if (self.horario!=None and (int(self.horario.dia )!= int(self.fecha.weekday()))):
                raise forms.ValidationError('El día y la fecha no coinciden')
            else:
                return self
        except:
            return self
            #raise forms.ValidationError('Horario no definido')
    class Meta:
        unique_together = ('horario', 'fecha',)