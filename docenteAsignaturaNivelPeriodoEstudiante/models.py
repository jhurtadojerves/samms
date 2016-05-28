# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from docenteAsignaturaNivelPeriodo.models import DocenteAsignaturaNivelPeriodo
from estudiante.models import Estudiante


from django.db import models

# Create your models here.

class DocenteAsignaturaNivelPeriodo(models.Model):
    iddocenteasignatura = models.ForeignKey(DocenteAsignaturaNivelPeriodo)
    idestudiante = models.ForeignKey(Estudiante)