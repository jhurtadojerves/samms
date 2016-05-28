# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Carrera(models.Model):
    codigo = models.CharField(max_length=32, unique=True)
    nombre = models.TextField(max_length=256)

