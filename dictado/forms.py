# -*- coding: utf-8 -*-
from django import forms
from models import Dictado
from django.core.exceptions import ValidationError

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
        model = Dictado
        exclude = ['horario','fecha', 'estado', 'revisado_por', 'comentario']