from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

from models import Periodo

import webservices

# Create your views here.

@staff_member_required
def consumir(request):

    if not (Periodo.objects.filter(estado=True).exists()):

        cliente = webservices.infoGeneral()
        resultado = cliente.service.GetPeriodoActual()
        p = Periodo()
        p.codigo = resultado['Codigo']
        p.descripcion = resultado['Descripcion']
        p.fechainicio =  resultado['FechaInicio']
        p.fechafin =  resultado['FechaFin']
        p.estado= True
        p.save()
        return JsonResponse(p, safe=False)
    else:
        return JsonResponse('lol',safe=False)