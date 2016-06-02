# -*- coding: utf-8 -*-

"""samms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import periodo.views, docente.views, estudiante.views


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', estudiante.views.home, name='home'),

    #URLs Migrar datos: Periodoy Asignaturas
    url(r'^migrar/datos/$', periodo.views.consumir, name='migrar_datos'),

    #URLs Docente
    url(r'^docentes/migrar/$', docente.views.migrar_docentes, name='migrar_docente'),

    #URLs Estudiantes
    url(r'^estudiantes/nuevo/$', estudiante.views.migrar_estudiante, name='migrar_estudiante'),
]
