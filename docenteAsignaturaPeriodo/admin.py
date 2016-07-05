# -*- coding: utf-8 -*-
from django.contrib import admin

from models import DocenteAsignaturaPeriodo

# Register your models here.

@admin.register(DocenteAsignaturaPeriodo)
class DocenteAsignaturaPeriodoAdmin(admin.ModelAdmin):
    list_display = ('docente', 'asignatura', 'periodo',)
    list_filter = ('docente', 'periodo', 'asignatura')
    raw_id_fields = ('docente', 'periodo', 'asignatura')
    ordering = ('docente', 'periodo')
    search_fields = ('asignatura__descripcion','docente__cedula', 'docente__first_name', 'docente__last_name')
