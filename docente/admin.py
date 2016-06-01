# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Docente

# Register your models here.

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('cedula','last_name', 'first_name',)
    #list_filter = ('abierta',)
    ordering = ('cedula', 'last_name',)
