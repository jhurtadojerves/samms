# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date
from django import forms

from docenteAsignaturaPeriodo.models import DocenteAsignaturaPeriodo



# Create your models here.

class Horario(models.Model):
	asignatura = models.ForeignKey(DocenteAsignaturaPeriodo, blank=True)
	dias = (
		('0', 'Lunes'),
		('1', 'Martes'),
		('2', 'Miercoles'),
		('3', 'Jueves'),
		('4', 'Viernes')
	)
	dia = models.CharField(max_length=1, choices=dias, default='0')

	horas_inicio = (
		('1', '07:30'),
		('2', '09:30'),
		('3', '11:30'),
		('4', '14:30'),
	)

	inicio = models.CharField(max_length=1, choices=horas_inicio, default='1')

	duracion = (
		('1', '1 Hora'),
		('2', '2 Horas')
	)

	fin = models.CharField(max_length=1, choices=duracion, default='2')

	def __unicode__(self):
		a = {0: 'Lunes', 1:'Martes', 2:'Miércoles', 3:'Jueves', 4: 'Viernes'}
		return self.asignatura.asignatura.descripcion + ' - ' + self.get_dia_display()

	class Meta:
		unique_together = ('asignatura', 'dia',)