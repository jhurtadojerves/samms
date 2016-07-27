# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Docente

# Register your models here.

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('cedula','last_name', 'first_name', 'is_active', 'is_staff' )
    #list_filter = ('abierta',)
    ordering = ('cedula', 'last_name',)
    list_editable = ('is_active', 'is_staff')
    search_fields = ('cedula', 'first_name', 'last_name')
