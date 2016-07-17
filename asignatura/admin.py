# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Asignatura

@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion', 'nivel', 'horas', 'carrera')
    list_filter = ('carrera', 'nivel',)
    ordering = ('carrera', 'nivel','descripcion', 'codigo',)
    search_fields = ('codigo', 'descripcion', 'nivel', 'carrera__nombre', 'carrera__codigo')

# Register your models here.
