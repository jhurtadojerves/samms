# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template.context import RequestContext
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required

from periodo.models import Periodo
from carrera.models import Carrera
from asignatura.models import Asignatura
from docenteAsignaturaPeriodo.models import DocenteAsignaturaPeriodo
from models import Docente
from django.contrib.auth.hashers import make_password

import webservices, metodos

# Create your views here.

def migrar_docentes(request):
    #Instancia de los Servicios Web de Información General
    clienteGeneral = webservices.infoGeneral()

    #Instancia de los servicios Web de Información de Carreras
    clienteCarrera = webservices.infoCarrera()

    carreras = Carrera.objects.filter(abierta=True)

    for c in carreras:

        asignaturas = Asignatura.objects.filter(carrera = c)

        docentesAsignatura = list()
        periodo = Periodo.objects.get(estado=True)
        for a in asignaturas:
            docenteResult = clienteCarrera.service.GetDictadosMateria(a.carrera.codigo, a.codigo)

            if (docenteResult):
                docenteFormat = metodos.recursive_asdict(docenteResult[0][0][3])

                if (Docente.objects.filter(cedula=docenteFormat['Cedula']).exists()):
                    docente = Docente.objects.get(cedula=docenteFormat['Cedula'])
                else:
                    docente = Docente()
                    docente.cedula = docenteFormat['Cedula']
                    docente.username = docenteFormat['Cedula']
                    docente.first_name = metodos.remover_acentos(docenteFormat['Nombres'])
                    docente.last_name = metodos.remover_acentos(docenteFormat['Apellidos'])
                    docente.email = docenteFormat['Email']
                    docente.is_active = 1
                    docente.is_superuser = 0
                    docente.is_staff = 0
                    docente.password = make_password(docenteFormat['Cedula'], salt=None, hasher='default')
                    docente.save()

                if not(DocenteAsignaturaPeriodo.objects.filter(docente=docente,asignatura=a,periodo=periodo).exists()):
                    doc = Docente.objects.get(cedula=docenteFormat['Cedula'])
                    docasig = DocenteAsignaturaPeriodo()
                    docasig.docente = doc
                    docasig.asignatura = a
                    docasig.periodo = periodo
                    docasig.save()
    return JsonResponse('correcto', safe=False)

def logout_v(request):
    logout(request)
    return render(request, 'index.html', {}, context_instance=RequestContext(request))

def home(request):
    return render(request, 'index.html', {}, context_instance=RequestContext(request))

def login(request):
    return render(request, 'login.html', {}, context_instance=RequestContext(request))