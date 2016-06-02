# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm

from carrera.models import Carrera
from django.http import JsonResponse
import re

c = Carrera.objects.filter(abierta = True)
options = list()

class EstudianteForm(forms.Form):
    cedula = forms.CharField(max_length=11, label='Cedula Estudiante', widget=forms.TextInput(attrs={'class': 'form-control'}))

    for i in c:
        options.append((i.codigo, i.nombre))
    carrera = forms.ChoiceField(choices=options)
    def clean_cedula(self):
        """
        Valída que sea Correcta la Cédula
        """
        ced = self.cleaned_data['cedula']
        ced2 = ced.replace('-', '')
        msg1 = 'La Cédula introducida no es válida'
        msg2 = 'Debe constar de 10 números y un guión antes de la última cifra'
        regex = '[0-9]{9,9}[-][0-9]'
        if(re.match(regex, ced)):
            valores = [ int(ced2[x]) * (2 - x % 2) for x in range(9) ]
            suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
            veri = 10 - (suma - (10 * (suma / 10)))
            if int(ced2[9]) == int(str(veri)[-1:]):
                return ced
            else:
                raise forms.ValidationError('Ingrese una cédula válida')
        else:
            raise forms.ValidationError('Ingrese una cédula con el formato 000000000-0')