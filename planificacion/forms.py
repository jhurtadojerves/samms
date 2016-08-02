# -*- coding: utf-8 -*-
from django import forms
from models import Tema, Unidad
from horario.models import Horario
from django.core.exceptions import ValidationError
forms.DateInput.input_type="date"
forms.TimeInput.input_type="time"
forms.DateTimeInput.input_type="datetime-local"


class RevisarTemaForm(forms.ModelForm):
	class Meta:
		model = Tema
		fields = ['estado', 'comentario',]

class DictadoFormDocente(forms.ModelForm):
	'''def clean(self):
		# Sobrecargar clean devuelve un diccionario con los campos
		data = self.cleaned_data
		#super(DictadoAdminForm, self).clean()
		if (int(data['horario'].dia )!= int(data['fecha'].weekday())):
			raise forms.ValidationError('El día y la fecha no coinciden')
		else:
			return data
	'''
	class Meta:
		model = Tema
		exclude = ['unidad', 'estado', 'revisado_por', 'comentario', 'aprobar_otra_fecha', 'razon_aprobar_otra_fecha']

	def __init__(self, query, *args, **kwargs):
		super(DictadoFormDocente, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
			})

		self.fields['horario'].queryset = query
		self.fields['horario'].empty_label = None

class HorarioForm(forms.ModelForm):
	class Meta:
		model = Horario
		exclude = ['asignatura']

	def __init__(self, *args, **kwargs):
		super(HorarioForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
			})

class UnidadForm(forms.ModelForm):
	class Meta:
		model = Unidad
		exclude = ['asignatura']

	def __init__(self, *args, **kwargs):
		super(UnidadForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
			})