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
	nombre = models.CharField(max_length=256, null=False)
	unidad = models.ForeignKey(Unidad, blank = True)
	horario = models.ForeignKey(Horario, blank = True)
	fecha = models.DateField(null=False, blank= True)
	estado_opciones = (
		('0', 'Sin Revisar'),
		('1', 'Aprobado'),
		('2', 'No Aprobado')
	)
	estado = models.CharField(max_length=1, choices=estado_opciones, default='0', blank=True)
	revisado_por = models.ForeignKey(Estudiante, null=True, blank=True)
	comentario = models.TextField(max_length=256, null=True, blank = True)
	razon_aprobar_otra_fecha = models.TextField(max_length=256, blank= True)
	aprobar_otra_fecha = models.BooleanField(default=False, blank=True)

	def tema_string(self):
		return dict(Tema.estado_opciones)[self.estado]

	def dia_string(self):
		return Tema.horario.get_dia_display()
	class Meta:
		unique_together = ('unidad', 'fecha',)