# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template.context import RequestContext
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import make_password

from forms import EstudianteForm
from models import Estudiante
from carrera.models import Carrera
from periodo.models import Periodo
from  asignatura.models import Asignatura
from docenteAsignaturaPeriodo.models import DocenteAsignaturaPeriodo
from docenteAsignaturaPeriodoEstudiante.models import DocenteAsignaturaPeriodoEstudiante

import webservices, metodos

# Create your views here.

def home(request):
    #return render(request, '', {}, context_instance=RequestContext(request))
    return JsonResponse('Bienvenidos al Sistema de Avance Curricular', safe=False)

def migrar_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            cedula= form['cedula'].value()
            carrera = Carrera.objects.get(codigo=form['carrera'].value())
            periodo = Periodo.objects.get(estado=True)
            clienteCarrera = webservices.infoCarrera()
            #si el estudiante no está regstrado en la base de datos lo buscamos en el OASIS y lo almacenamos en la base de datos local
            if not (Estudiante.objects.filter(cedula = cedula).exists()):
                estudiante = Estudiante()
                estudiante.cedula = cedula
                resultEstudiante = clienteCarrera.service.GetDatosEstudianteMatriculado(estudiante.cedula)

                if resultEstudiante is not None:
                    estudiante.cedula = resultEstudiante['Cedula']
                    estudiante.username = resultEstudiante['Cedula']
                    estudiante.first_name = metodos.remover_acentos(resultEstudiante['Nombres'])
                    estudiante.last_name = metodos.remover_acentos(resultEstudiante['Apellidos'])
                    if not resultEstudiante['Email'] is None:
                        estudiante.email = resultEstudiante['Email']
                    estudiante.is_active = 1
                    estudiante.is_superuser = 0
                    estudiante.is_staff = 0
                    estudiante.password = make_password(resultEstudiante['Cedula'], salt=None, hasher='default')
                    estudiante.save()
                    #return JsonResponse(estudiante.first_name, safe=False)
            #si el estudiante existe en la base de datos lo recuperamos

            if(Estudiante.objects.filter(cedula=cedula)):

                estudiante = Estudiante.objects.get(cedula=cedula)
                #Obtenemos las asignaturas en las que el estudiante se encuentra matriculado desde la base de datos del sistema académico
                resultAsignaturas = clienteCarrera.service.GetMateriasEstudiante(carrera.codigo, estudiante.cedula, periodo.codigo)
                #return JsonResponse((resultAsignaturas != ""), safe=False)
                if (resultAsignaturas != ""):
                    for a in resultAsignaturas[0]:

                        tmp = metodos.recursive_asdict(a)

                        if Asignatura.objects.filter(codigo = tmp['Codigo']).exists():
                            asignatura = Asignatura.objects.get(codigo=tmp['Codigo'])

                            if DocenteAsignaturaPeriodo.objects.filter(asignatura = asignatura, periodo = periodo).exists():

                                docenteAsignatura = DocenteAsignaturaPeriodo.objects.get(asignatura = asignatura, periodo = periodo)
                                if not (DocenteAsignaturaPeriodoEstudiante.objects.filter(docenteasignatura = docenteAsignatura, estudiante = estudiante).exists()):
                                    docenteAsignaturaEstudiante = DocenteAsignaturaPeriodoEstudiante()
                                    docenteAsignaturaEstudiante.docenteasignatura = docenteAsignatura
                                    docenteAsignaturaEstudiante.estudiante = estudiante
                                    docenteAsignaturaEstudiante.save()
            return JsonResponse('Hail Hydra', safe=False)






            #return HttpResponseRedirect(reverse('docente_inasistencia_materia', args=(codigoasignatura,)))

    else:
        form = EstudianteForm()
    return render(request, 'nuevo.html', {'form':form}, context_instance=RequestContext(request))