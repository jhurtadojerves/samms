# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Periodo(models.Model):
    codigo = models.CharField(max_length=8, unique=True)
    fechainicio = models.DateTimeField()
    fechafin = models.DateTimeField()
    descripcion = models.TextField(max_length=32)
    estado = models.BooleanField(default=True)
