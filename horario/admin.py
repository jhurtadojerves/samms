# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Horario

# Register your models here.

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('asignatura','dia', 'inicio', 'fin',)
    #list_filter = (('asignatura', admin.RelatedOnlyFieldListFilter),)
    raw_id_fields = ('asignatura',)
    ordering = ('asignatura', 'dia',)


