# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from docenteAsignaturaPeriodo.models import DocenteAsignaturaPeriodo
from estudiante.models import Estudiante


from django.db import models

# Create your models here.

class DocenteAsignaturaPeriodoEstudiante(models.Model):
    iddocenteasignatura = models.ForeignKey(DocenteAsignaturaPeriodo)
    idestudiante = models.ForeignKey(Estudiante)