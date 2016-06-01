# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Carrera
# Register your models here.


@admin.register(Carrera)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'abierta',)
    list_filter = ('abierta',)
    ordering = ('abierta', 'codigo', 'nombre', )