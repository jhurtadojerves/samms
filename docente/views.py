# -*- coding: utf-8 -*-
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages import error

from periodo.models import Periodo
from carrera.models import Carrera
from asignatura.models import Asignatura
from docenteAsignaturaPeriodo.models import DocenteAsignaturaPeriodo
from models import Docente
from planificacion.models import Tema, Unidad
from horario.models import Horario

from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from planificacion.forms import DictadoFormDocente, UnidadForm

import datetime

import webservices, metodos

# Create your views here.
@staff_member_required
def migrar_docentes(request):
    try:

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
                        if not docenteFormat['Email'] is None:
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
        return HttpResponse('Docentes Registrados Correctamente')
    except Exception as e:
        return HttpResponse(e.args, e)

@login_required()
def logout_v(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
    #return render(request, 'index.html', {}, context_instance=RequestContext(request))

def home(request):
    return render(request, '../templates/index.html', {}, context_instance=RequestContext(request))

def login(request):
    return render(request, '../templates/login.html', {}, context_instance=RequestContext(request))

@login_required()
def ver_asignaturas(request):
    periodo = Periodo.objects.get(estado=True)
    docente = request.user
    docasig = DocenteAsignaturaPeriodo.objects.filter(docente=docente, periodo=periodo)

    asignaturas = list()

    for asignatura in docasig:
        asignaturas.append(asignatura.asignatura)

    return render(request, 'planificacion/ver_materias.html',{'asignaturas': asignaturas}, context_instance=RequestContext(request))

@login_required()
def ver_unidad(request, id):
    periodo = get_object_or_404(Periodo, estado = True)
    asignatura = get_object_or_404(Asignatura, codigo = id)
    docente = get_object_or_404(Docente, user_ptr = request.user)
    docasigper = get_object_or_404(DocenteAsignaturaPeriodo, docente = docente, periodo = periodo, asignatura = asignatura)
    unidades = Unidad.objects.filter(asignatura = docasigper)
    return render(request, 'planificacion/ver_unidades.html',{'unidades': unidades, 'asignatura': asignatura}, context_instance=RequestContext(request))

@login_required()
def ingresar_unidad(request, id):
    periodo = get_object_or_404(Periodo, estado = True)
    asignatura = get_object_or_404(Asignatura, codigo = id)
    docente = get_object_or_404(Docente, user_ptr = request.user)
    docasigper = get_object_or_404(DocenteAsignaturaPeriodo, docente = docente, periodo = periodo, asignatura = asignatura)

    if request.method == 'POST':
        form = UnidadForm(request.POST)

        if form.is_valid():
            unidad = form.save(commit=False)
            unidad.asignatura = docasigper
            unidad.save()
            return HttpResponseRedirect(reverse('ver_unidad', args=(id,)))
    else:
        form = UnidadForm()
    return render(request, 'planificacion/crear_unidad.html', {'form': form}, context_instance=RequestContext(request))

@login_required()
def ver_temas(request, asig, uni):
    asignatura = get_object_or_404(Asignatura, codigo = asig)
    unidad = get_object_or_404(Unidad, id = uni)
    docasigper = unidad.asignatura
    temas = Tema.objects.filter(unidad = unidad)
    return render(request, 'planificacion/ver_temas.html', {'temas':temas, 'asignatura':asignatura, 'unidad':unidad}, context_instance=RequestContext(request))

@login_required()
def nuevo_tema(request, asig, uni):
    unidad = get_object_or_404(Unidad, id = uni)
    docasigper = unidad.asignatura
    if request.method == 'POST':
        form = DictadoFormDocente(request.POST)
        tema = form.save(commit=False)
        tema.descripcion = request.POST['descripcion']
        tema.unidad = unidad
        horario = get_object_or_404(Horario, id = request.POST['horario'])
        tema.horario = horario
        tema.fecha = request.POST['fecha']

        date = datetime.datetime.strptime(tema.fecha, '%Y-%m-%d')


        if(int(horario.dia) == int(date.weekday())):
            tema.save()
            response = HttpResponseRedirect(reverse('ver_temas', args=(asig, uni,))+"?mensaje=correcto")
            return response
        else:
            error = 'El día y la fecha no coinciden'
            return render(request, 'planificacion/ingresa_tema.html', {'form': form}, context_instance=RequestContext(request))
            #return render(request, 'planificacion/error_ingresar_dictado.html', {'error': error}, context_instance=RequestContext(request))
    else:
        form = DictadoFormDocente(query = Horario.objects.filter(asignatura = docasigper))
    return render(request, 'planificacion/ingresa_tema.html', {'form': form}, context_instance=RequestContext(request))

def ingresar_dictado(request, asignatura):
    if request.method == 'POST':
        form = DictadoFormDocente(request.POST)

        if form.is_valid():
            docente = request.user
            asignatura = Asignatura.objects.get(codigo=asignatura)
            periodo = Periodo.objects.get(estado=True)
            docasig = DocenteAsignaturaPeriodo.objects.get(docente=docente,periodo=periodo,asignatura=asignatura)
            horario = Horario.objects.get(asignatura=docasig, dia = datetime.datetime.now().weekday())
            fecha = datetime.datetime.now()
            dictado = form.save(commit=False)

            dictado.horario = horario
            dictado.fecha = fecha
            dictado.estado = 0 #Sin Revisa
            dictado.save()
            return render(request, 'planificacion/ingresar_dictado_correcto.html', {'dictado': dictado}, context_instance=RequestContext(request))

    else:
        if(Asignatura.objects.filter(codigo=asignatura).exists()):
            docente = request.user
            asignatura = Asignatura.objects.get(codigo=asignatura)
            periodo = Periodo.objects.get(estado=True)
            if(DocenteAsignaturaPeriodo.objects.filter(docente=docente,periodo=periodo,asignatura=asignatura).exists()):
                docasig = DocenteAsignaturaPeriodo.objects.get(docente=docente,periodo=periodo,asignatura=asignatura)
                if (Horario.objects.filter(asignatura=docasig, dia = datetime.datetime.now().weekday()).exists()):
                    horario = Horario.objects.get(asignatura=docasig, dia = datetime.datetime.now().weekday())
                    if not (Tema.objects.filter(fecha = datetime.datetime.now(), horario=horario ).exists()):
                        form = DictadoFormDocente()
                        return render(request, 'planificacion/ingresa_dictado.html', {'form': form}, context_instance=RequestContext(request))
                    else:
                        error ='La asignatura '+asignatura.descripcion + ' ya cuenta con un tema registrado hoy'
                else:
                    error = 'La asignatura '+asignatura.descripcion+' no registra horario para el dia de hoy'
            else:
                error = 'El docente ' + request.user.get_full_name() + ' no tiene registrada la asignatura ' +asignatura.descripcion
        else:
            raise Http404
    return render(request, 'planificacion/error_ingresar_dictado.html', {'error': error}, context_instance=RequestContext(request))