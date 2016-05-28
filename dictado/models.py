# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from horario.models import Horario

# Create your models here.

class Dictado(models.Model):
    horario = models.ForeignKey(Horario)
    unidad = models.SmallIntegerField()
    tema = models.TextField(max_length=256, null=False, blank=False)
    fecha = models.DateField(null=False)
    estado_opciones = (
        ('0', 'Sin Revisar'),
        ('1', 'Aprobado'),
        ('2', 'No Aprobado')
    )
    estado = models.CharField(max_length=1, choices=estado_opciones, default='0')
    comentario = models.CharField(max_length=255)


