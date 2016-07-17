# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, Group

from django.db import models


# Create your models here.

class Docente(User):
	cedula = models.CharField(unique=True, max_length=16)

	def __unicode__(self):
		return self.first_name + " " + self.last_name