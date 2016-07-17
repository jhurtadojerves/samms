# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Periodo


# Register your models here.

@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion', 'estado' )
    list_filter = ('codigo', 'estado')
    ordering = ('codigo',)
