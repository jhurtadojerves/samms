# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.urlresolvers import reverse

from forms import EstudianteForm

from planificacion.forms import RevisarTemaForm

from models import Estudiante
from carrera.models import Carrera
from periodo.models import Periodo
from  asignatura.models import Asignatura
from docenteAsignaturaPeriodo.models import DocenteAsignaturaPeriodo
from docenteAsignaturaPeriodoEstudiante.models import DocenteAsignaturaPeriodoEstudiante
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

import webservices, metodos

from planificacion.models import Tema, Unidad
from docenteAsignaturaPeriodo.models import DocenteAsignaturaPeriodo

# Create your views here.


@staff_member_required
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
    return render(request, '../templates/estudiante/nuevo.html', {'form':form}, context_instance=RequestContext(request))

@login_required()
def ver_temas_estudiante(request):
    estudiante = get_object_or_404(Estudiante, user_ptr = request.user)
    periodo = get_object_or_404(Periodo, estado=True)
    asignaturas = DocenteAsignaturaPeriodo.objects.filter(periodo=periodo)
    asigEstudiante = DocenteAsignaturaPeriodoEstudiante.objects.filter(estudiante = estudiante)
    lista = list()
    for i in asigEstudiante:
        lista.append(i.docenteasignatura)
    unidad = Unidad.objects.filter(asignatura__in = lista)
    temas = Tema.objects.filter(fecha = timezone.now(), unidad__in = unidad, estado=0).order_by('unidad', 'fecha') | Tema.objects.filter(aprobar_otra_fecha = True, unidad__in = unidad, estado = 0)
    return render(request, 'estudiante/ver_temas.html', {'temas':temas}, context_instance=RequestContext(request))

def revisar_tema(request, id):
    tema = get_object_or_404(Tema, id = id)
    estudiante = get_object_or_404(Estudiante, user_ptr = request.user)
    if request.method == 'POST':
        form = RevisarTemaForm(request.POST, instance=tema)
        if form.is_valid():
            revisar = form.save(commit=False)
            if int(revisar.estado) != 0:
                revisar.revisado_por = estudiante
                revisar.aprobar_otra_fecha = False
                revisar.save()
            return HttpResponseRedirect(reverse('ver_temas_estudiante')+"?mensaje=correcto")
    else:
        form = RevisarTemaForm(instance=tema)
    return render(request, 'estudiante/revisar_tema.html', {'form':form}, context_instance=RequestContext(request))