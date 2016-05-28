# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from horario.models import Horario

# Create your models here.

class Planificacion(models.Model):
    horario = models.ForeignKey(Horario)
    unidad = models.SmallIntegerField()
    tema = models.TextField(max_length=256, null=False, blank=False)
    fecha = models.DateField(null=False)