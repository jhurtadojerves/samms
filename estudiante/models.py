# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class Estudiante(User):
    cedula = models.CharField(unique=True, max_length=16)