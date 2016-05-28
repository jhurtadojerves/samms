# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from carrera.models import Carrera

# Create your models here.

class Asignatura(models.Model):
    codigo = models.CharField(max_length=32, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    nivel =  models.CharField(max_length=16, blank=True, null=True)
    horas = models.IntegerField()
    carrera = models.ForeignKey(Carrera)