# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Dictado
#from forms import DictadoAdminForm

# Register your models here.

@admin.register(Dictado)
class DictadoAdmin(admin.ModelAdmin):
    list_display = ('horario','fecha', 'tema', 'unidad','estado',)
    list_filter = ('fecha', 'estado',)
    search_fields = ('estado',)
    ordering = ('horario', 'fecha', 'estado',)