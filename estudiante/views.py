# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.template.context import RequestContext
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.db.models import Q

from wkhtmltopdf.views import PDFTemplateResponse

from forms import EstudianteForm, FechasReporte

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
from horario.models import Horario


from reportlab.platypus import Paragraph
from reportlab.platypus import Image
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table

import time

# Create your views here.


@staff_member_required
def migrar_estudiante(request):
	try:
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
						usuario = User.objects.get(id = estudiante.id)
						if Group.objects.filter(name='Estudiantes').exists():
							grupo = Group.objects.get(name='Estudiantes')
						else:
							grupo = Group.objects.create(name='Estudiantes')
						usuario.groups.add(grupo)
						usuario.save()

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
				return HttpResponseRedirect(reverse('home') + "?migrar=correcto")
		else:
			form = EstudianteForm()
		return render(request, 'estudiante/nuevo.html', {'form':form}, context_instance=RequestContext(request))
	except:
		return HttpResponseRedirect(reverse('home') + "?migrar=error")

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

	tema = get_object_or_404(Tema, Q(fecha = timezone.now()) | Q(aprobar_otra_fecha = True), id = id)

	estudiante = get_object_or_404(Estudiante, user_ptr = request.user)
	periodo = get_object_or_404(Periodo, estado=True)
	asignaturas = DocenteAsignaturaPeriodo.objects.filter(periodo=periodo, asignatura=tema.horario.asignatura.asignatura)
	asigEstudiante = DocenteAsignaturaPeriodoEstudiante.objects.filter(estudiante=estudiante)
	if not (
	DocenteAsignaturaPeriodoEstudiante.objects.filter(estudiante=estudiante, docenteasignatura__in=asignaturas).exists()):
		raise Http404()

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
	return render(request, 'estudiante/revisar_tema.html', {'form':form, 'tema':tema}, context_instance=RequestContext(request))

def ver_materia_reportes(request, id):
	estudiante = get_object_or_404(Estudiante, user_ptr=request.user)
	periodo = get_object_or_404(Periodo, estado=True)
	asignatura = get_object_or_404(Asignatura, codigo = id)
	asignaturas = DocenteAsignaturaPeriodo.objects.filter(periodo=periodo, asignatura = id)
	asigEstudiante = DocenteAsignaturaPeriodoEstudiante.objects.filter(estudiante=estudiante, asignatura = id)
	lista = list()
	for i in asigEstudiante:
		lista.append(i.docenteasignatura)
	unidad = Unidad.objects.filter(asignatura__in=lista)
	temas = Tema.objects.filter(fecha=timezone.now(), unidad__in=unidad, estado=0).order_by('unidad', 'fecha')
	return render(request, 'estudiante/ver_temas.html', {'temas': temas}, context_instance=RequestContext(request))


def ver_materia_reporte(request):
	estudiante = get_object_or_404(Estudiante, user_ptr=request.user)
	periodo = get_object_or_404(Periodo, estado=True)
	#asignatura = get_object_or_404(Asignatura, codigo = id)
	asignaturas = DocenteAsignaturaPeriodo.objects.filter(periodo=periodo)
	asigEstudiante = DocenteAsignaturaPeriodoEstudiante.objects.filter(estudiante=estudiante)
	lista = list()
	for i in asigEstudiante:
		lista.append(i.docenteasignatura.asignatura)
	return render(request, 'estudiante/ver_asignaturas.html', {'asignaturas': lista}, context_instance=RequestContext(request))

def ver_reporte_input_fechas(request, id):
	estiloHoja = getSampleStyleSheet()
	cabecera = estiloHoja['Heading4']
	cabecera.pageBreakBefore = 0
	cabecera.keepWithNext = 0
	estilo = estiloHoja['BodyText']
	story = []

	fichero_imagen = "elviajedelnavegante_png.png"
	imagen_logo = Image("logo.png", width=400, height=100)
	story.append(imagen_logo)
	story.append(Spacer(0, 10))


	estudiante = get_object_or_404(Estudiante, user_ptr = request.user)
	asignatura = get_object_or_404(Asignatura, codigo = id)
	periodo = get_object_or_404(Periodo, estado = True)
	asigperiodo = DocenteAsignaturaPeriodo.objects.filter(asignatura = asignatura, periodo = periodo)
	asigestudiante = DocenteAsignaturaPeriodoEstudiante.objects.filter(docenteasignatura__in=asigperiodo, estudiante = estudiante)




	aux = list()
	for i in asigestudiante:
		aux.append(i.docenteasignatura)
	horario = Horario.objects.filter(asignatura__in = aux)


	if request.method == 'POST':
		form = FechasReporte(request.POST)

		if form.is_valid():
			inicio =  form['inicio'].value()
			fin = form['fin'].value()
			temas = Tema.objects.filter(horario__in=horario, fecha__range = (inicio, fin))


			datos = []

			#horario = Horario.objects.filter(asignatura=i)
			#temas = Tema.objects.filter(horario__in=horario, fecha__range=(periodo.fechainicio, periodo.fechafin))
			if temas.exists():
				parrafo = Paragraph(asignatura.descripcion, cabecera)
				fila_inicial = ['Tema', 'Fecha', 'Hora', 'Estado', 'Revisado por']
				story.append(parrafo)
				datos.append(fila_inicial)

				for t in temas:
					try:
						fila = [t.nombre, t.fecha, t.horario.get_inicio_display(), t.get_estado_display(),
								t.revisado_por.get_full_name()]
					except:
						fila = [t.nombre, t.fecha, t.horario.get_inicio_display(), t.get_estado_display(), '-']
					datos.append(fila)
				tabla = Table(datos)
				tabla.normalizeData(datos)
				tabla.setStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)])
				tabla.setStyle([('BOX', (0, 0), (-1, -1), 0.25, colors.black)])

				story.append(tabla)
				story.append(Spacer(0, 20))
			ahora = time.strftime("%x %X")
			parrafo = Paragraph("Generado por: "+estudiante.get_full_name(), cabecera)
			story.append(parrafo)
			story.append(Spacer(0, 10))
			parrafo = Paragraph(ahora, cabecera)
			story.append(parrafo)

			parrafo = Paragraph("Generado por: " + estudiante.get_full_name() + " " + ahora, cabecera)

			doc = SimpleDocTemplate(estudiante.cedula + "-"+asignatura.codigo+".pdf", pagesize=A4, showBoundary=0)
			doc.build(story)
			output = open(estudiante.cedula + "-"+asignatura.codigo+".pdf")
			response = HttpResponse(output, content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename=' + estudiante.cedula + "-"+asignatura.codigo+".pdf"
			return response

			#return PDFTemplateResponse(request, "reportes/estudiante.html", {'temas': temas, 'asignatura': asignatura})
	else:
		form = FechasReporte()
	return render(request, 'estudiante/form_reporte.html', {'form': form}, context_instance=RequestContext(request))