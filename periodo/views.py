# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

from models import Periodo
from carrera.models import Carrera
from asignatura.models import Asignatura

import webservices, metodos

import sys

# Create your views here.

@staff_member_required
def consumir(request):
    try:
        #Instancia de los Servicios Web de Información General
        clienteGeneral = webservices.infoGeneral()
        #Instancia de los servicios Web de Información de Carreras
        clienteCarrera = webservices.infoCarrera()

        #Obtiene todos los periodos académicos activos
        periodos = Periodo.objects.filter(estado=True)

        if (periodos.exists()):
            for i in periodos:
                #Setea en False todos los periodos académicos
                i.estado = False

        #Obtenemos el periodo académico actual
        resultadoPeriodo = clienteGeneral.service.GetPeriodoActual()

        #Instanciamos un Periodo en blanco y lo llenamos con el Periodo obtenido
        p = Periodo()
        p.codigo = resultadoPeriodo['Codigo']
        p.descripcion = resultadoPeriodo['Descripcion']
        p.fechainicio =  resultadoPeriodo['FechaInicio']
        p.fechafin =  resultadoPeriodo['FechaFin']

        #Definimos el periodo actual como activo
        p.estado= True

        #Si no existe un periodo con el código obtenido lo guardamos en la base de datos
        if not (Periodo.objects.filter(codigo=p.codigo).exists()):
            p.save()
        else:
            #De existir, se actualizan los datos y se guarda el periodo modificado
            pDB = Periodo.objects.get(codigo=p.codigo)
            pDB.descripcion = p.descripcion
            pDB.fechainicio = p.fechainicio
            pDB.fechafin = p.fechafin
            pDB.estado = p.estado
            pDB.save()

        #Obtener Datos de las Carreras
        carreras = Carrera.objects.filter(abierta=True)

        #Si existen carreras registradas en la DB continuamos con el proceso de migración
        if(carreras.exists()):
            for c in carreras:
                asignaturas = list()
                resultadoMalla = clienteCarrera.service.GetMallaCurricularPensumVigenteSinDescripcion(c.codigo)

                #convertimos los datos obtenidos a un diccionario
                asignaturasOUT = metodos.recursive_asdict(resultadoMalla)

                #recorremos la estructura de datos para obtener las materias de forma individual
                for j in asignaturasOUT['Materia_Pensum']:

                    #Obtenemos los datos que deseamos
                    aux = [j['CodMateria'], metodos.remover_acentos(j['Materia']),j['HorasPracticas']+j['HorasTeoricas'],j['Nivel'],c]
                    #Guardamos las materias en una lista
                    asignaturas.append(aux)
                for k in asignaturas:
                    if not (Asignatura.objects.filter(codigo=k[0]).exists()):
                        asig = Asignatura()
                        asig.codigo = k[0]
                        asig.descripcion =  k[1]
                        asig.horas = k[2]
                        asig.nivel = k[3]
                        asig.carrera = c
                        asig.save()
        return JsonResponse('Todo bien <3', safe=False)
    except:
        return JsonResponse('Todo mal </3', safe=False)