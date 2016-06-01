# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template.context import RequestContext

# Create your views here.

def home(request):
    return render(request, 'prueba.html', {}, context_instance=RequestContext(request))