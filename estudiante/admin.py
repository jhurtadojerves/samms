# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Estudiante

# Register your models here.

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('cedula','last_name', 'first_name',)
    #list_filter = ('abierta',)
    ordering = ('cedula', 'last_name',)