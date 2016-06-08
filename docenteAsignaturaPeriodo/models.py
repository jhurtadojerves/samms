# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from docente.models import Docente
from periodo.models import Periodo
from asignatura.models import Asignatura

from django.db import models

# Create your models here.

class DocenteAsignaturaPeriodo(models.Model):
    docente = models.ForeignKey(Docente)
    periodo = models.ForeignKey(Periodo)
    asignatura = models.ForeignKey(Asignatura)

    class Meta:
        unique_together = ('asignatura', 'periodo',)

    def __str__(self):
        return self.docente.get_full_name() + " - " + self.asignatura.descripcion