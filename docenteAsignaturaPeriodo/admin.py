# -*- coding: utf-8 -*-
from django.contrib import admin

from models import DocenteAsignaturaPeriodo

# Register your models here.

@admin.register(DocenteAsignaturaPeriodo)
class DocenteAsignaturaPeriodoAdmin(admin.ModelAdmin):
    list_display = ('docente', 'asignatura', 'periodo',)
    list_filter = ('docente', 'periodo',)
    ordering = ('docente', 'periodo')
