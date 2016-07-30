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
from django.contrib.auth.views import login
#Comentar línea de abajo para la migración inicial
#import periodo.views, docente.views, estudiante.views

#from asignatura.models import Asignatura

#from docente.views import coordinador_reporte_materias_todo_xls, coordinador_asignaturas_xls

#Comentar URLs de abajo para la migración inicial
urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #URLS login, logout, cambiar contraseña
    url(r'^login/$', login, {'template_name': 'login.html', }, name='login'),
    url(r'^logout$', 'docente.views.logout_v', name='logout'),
    url(r'^perfil/contrasena/$', 'django.contrib.auth.views.password_change', {'post_change_redirect' : '/','template_name': 'password.html'},name='contrasena'),
    url(r'^$', 'docente.views.home', name='home'),

    #URLs Migrar datos: Periodoy Asignaturas
    url(r'^migrar/datos/$', 'periodo.views.consumir', name='migrar_datos'),
    url(r'^migrar/docentes/$', 'docente.views.migrar_docentes', name='migrar_docente'),
    url(r'^migrar/estudiantes/$', 'estudiante.views.migrar_estudiante', name='migrar_estudiante'),

    #URLs Docente
    url(r'^docente/asignatura/$', 'docente.views.ver_asignaturas', name='ver_asignaturas'),
    url(r'^docente/asignatura/([^/]+)/$', 'docente.views.ver_unidad', name='ver_unidad'),
    url(r'^docente/asignatura/([^/]+)/unidad/crear/$', 'docente.views.ingresar_unidad', name='ingresar_unidad'),
    url(r'^docente/asignatura/([^/]+)/unidad/([^/]+)/$', 'docente.views.ver_temas', name='ver_temas'),
    url(r'^docente/asignatura/([^/]+)/unidad/([^/]+)/tema/nuevo/$', 'docente.views.nuevo_tema', name='nuevo_tema'),
	url(r'^docente/reportes/$','docente.views.ver_materia_reporte',name= "docente_ver_materia_reporte"),
	url(r'^docente/reportes/([^/]+)/$','docente.views.ver_reporte_input_fechas',name= "docente_ver_reporte_input_fechas"),
    #URLs Estudiantes

    url(r'^estudiante/temas/$', 'estudiante.views.ver_temas_estudiante', name='ver_temas_estudiante'),
    url(r'^estudiante/temas/revisar/([^/]+)/$', 'estudiante.views.revisar_tema', name='revisar_tema'),
	url(r'^estudiante/reportes/$','estudiante.views.ver_materia_reporte',name= "ver_materia_reporte"),
	url(r'^estudiante/reportes/([^/]+)/$','estudiante.views.ver_reporte_input_fechas',name= "ver_reporte_input_fechas"),

	#URLs coordinador académico
	url(r'^reportes/$', 'docente.views.coordinador_buscar_docentes', name = 'coordinador_buscar_docentes'),
	url(r'^reportes/buscar/$', 'docente.views.busqueda', name='busqueda'),
	url(r'^reportes/docente/([^/]+)/$', 'docente.views.coordinador_reporte_materias', name = 'coordinador_reporte_materias'),
	url(r'^reportes/docente/([^/]+)/pdf/$', 'docente.views.coordinador_reporte_materias_todo', name = 'coordinador_reporte_materias_todo'),

	#url(r'^reportes/xls/descargar/$', 'coordinador_reporte_materias_todo_xls.as_view()', name = 'coordinador_reporte_materias_todo_xls'),
	url(r'^reportes/xls/$', 'docente.views.coordinador_buscar_docentes_excel', name = 'coordinador_buscar_docentes_excel'),
	url(r'^reportes/xls/docente/([^/]+)/$', 'docente.views.coordinador_asignaturas_xls', name = 'coordinador_asignaturas_xls'),
	url(r'^reportes/xls/docente/([^/]+)/([^/]+)/$', 'docente.views.coordinador_asignaturas_xls_asig', name = 'coordinador_asignaturas_xls_asig'),


]
