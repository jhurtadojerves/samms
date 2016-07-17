# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Tema, Unidad


# Register your models here.

@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'fecha', 'estado', 'aprobar_otra_fecha']
    raw_id_fields = ('unidad', 'horario')
    list_editable = ['aprobar_otra_fecha',]

@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'asignatura']
    raw_id_fields = ('asignatura',)
