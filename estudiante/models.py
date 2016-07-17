# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, Group

from django.db import models

# Create your models here.
class Estudiante(User):
    cedula = models.CharField(unique=True, max_length=16)

    def clean(self):
        if (Group.objects.filter(name='Estudiantes').exists()):
            grupo = Group.objects.get(name='Estudiantes')
            self.user.groups.add(grupo)
        else:
            grupo = Group.objects.create(name="Estudiantes")
            self.user.groups.add(grupo)
        return self