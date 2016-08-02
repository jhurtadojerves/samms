# -*- coding: utf-8 -*-
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages import error
from django.contrib.auth.models import User, Group

from periodo.models import Periodo
from carrera.models import Carrera
from asignatura.models import Asignatura
from docenteAsignaturaPeriodo.models import DocenteAsignaturaPeriodo
from models import Docente
from planificacion.models import Tema, Unidad
from horario.models import Horario

from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from planificacion.forms import DictadoFormDocente, UnidadForm, HorarioForm
from estudiante.forms import FechasReporte
from wkhtmltopdf.views import PDFTemplateResponse
from django import forms
import datetime


import xlsxwriter
from xlsxwriter.utility import xl_range_abs
from django.views.generic import View

import webservices, metodos


# Create your views here.
@staff_member_required
def migrar_docentes(request):
	try:

		# Instancia de los Servicios Web de Información General
		clienteGeneral = webservices.infoGeneral()

		# Instancia de los servicios Web de Información de Carreras
		clienteCarrera = webservices.infoCarrera()

		carreras = Carrera.objects.filter(abierta=True)

		for c in carreras:

			asignaturas = Asignatura.objects.filter(carrera=c)

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
						if Group.objects.filter(name='Docentes').exists():
							grupo = Group.objects.get(name='Docentes')
						else:
							grupo = Group.objects.create(name='Docentes')
						# docente.groups.add()
						docente.save()
						usuario = User.objects.get(id=docente.id)
						usuario.groups.add(grupo)
						usuario.save()

					if not (
					DocenteAsignaturaPeriodo.objects.filter(docente=docente, asignatura=a, periodo=periodo).exists()):
						doc = Docente.objects.get(cedula=docenteFormat['Cedula'])
						docasig = DocenteAsignaturaPeriodo()
						docasig.docente = doc
						docasig.asignatura = a
						docasig.periodo = periodo
						docasig.save()
		return HttpResponseRedirect(reverse('home') + "?migrar=correcto")
	except Exception as e:
		# return HttpResponse(e)
		return HttpResponseRedirect(reverse('home') + "?migrar=error")


@login_required()
def logout_v(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))


# return render(request, 'index.html', {}, context_instance=RequestContext(request))

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

	return render(request, 'planificacion/ver_materias.html', {'asignaturas': asignaturas},
				  context_instance=RequestContext(request))


@login_required()
def ver_unidad(request, id):
	periodo = get_object_or_404(Periodo, estado=True)
	asignatura = get_object_or_404(Asignatura, codigo=id)
	docente = get_object_or_404(Docente, user_ptr=request.user)
	docasigper = get_object_or_404(DocenteAsignaturaPeriodo, docente=docente, periodo=periodo, asignatura=asignatura)
	unidades = Unidad.objects.filter(asignatura=docasigper)
	return render(request, 'planificacion/ver_unidades.html', {'unidades': unidades, 'asignatura': asignatura},
				  context_instance=RequestContext(request))


@login_required()
def ingresar_unidad(request, id):
	periodo = get_object_or_404(Periodo, estado=True)
	asignatura = get_object_or_404(Asignatura, codigo=id)
	docente = get_object_or_404(Docente, user_ptr=request.user)
	docasigper = get_object_or_404(DocenteAsignaturaPeriodo, docente=docente, periodo=periodo, asignatura=asignatura)

	if request.method == 'POST':
		form = UnidadForm(request.POST)

		if form.is_valid():
			unidad = form.save(commit=False)
			unidad.asignatura = docasigper
			unidad.save()
			return HttpResponseRedirect(reverse('ver_unidad', args=(id,)))
	else:
		form = UnidadForm()
	return render(request, 'planificacion/crear_unidad.html', {'form': form, 'asignatura': asignatura}, context_instance=RequestContext(request))


@login_required()
def ver_temas(request, asig, uni):
	asignatura = get_object_or_404(Asignatura, codigo=asig)
	unidad = get_object_or_404(Unidad, id=uni)
	docasigper = unidad.asignatura
	temas = Tema.objects.filter(unidad=unidad)
	return render(request, 'planificacion/ver_temas.html', {'temas': temas, 'asignatura': asignatura, 'unidad': unidad},
				  context_instance=RequestContext(request))


@login_required()
def nuevo_tema(request, asig, uni):
	unidad = get_object_or_404(Unidad, id=uni)
	docasigper = unidad.asignatura
	query = Horario.objects.filter(asignatura=docasigper)
	form = DictadoFormDocente(query, request.POST)
	bandera = False
	if request.method == 'POST':
		if form.is_valid():
			tema = form.save(commit=False)
			tema.descripcion = request.POST['nombre']
			tema.unidad = unidad
			horario = get_object_or_404(Horario, id=request.POST['horario'])
			tema.horario = horario
			tema.fecha = request.POST['fecha']

			date = datetime.datetime.strptime(tema.fecha, '%Y-%m-%d')

			if (int(horario.dia) == int(date.weekday())):
				tema.save()
				response = HttpResponseRedirect(reverse('ver_temas', args=(asig, uni,)) + "?mensaje=correcto")
				return response
			else:
				bandera = True


		# return render(request, 'planificacion/error_ingresar_dictado.html', {'error': error}, context_instance=RequestContext(request))
	else:
		form = DictadoFormDocente(query=Horario.objects.filter(asignatura=docasigper))
	return render(request, 'planificacion/ingresa_tema.html', {'form': form, 'bandera': bandera, 'unidad': unidad}, context_instance=RequestContext(request))


def ingresar_dictado(request, asignatura):
	if request.method == 'POST':
		form = DictadoFormDocente(request.POST)

		if form.is_valid():
			docente = request.user
			asignatura = Asignatura.objects.get(codigo=asignatura)
			periodo = Periodo.objects.get(estado=True)
			docasig = DocenteAsignaturaPeriodo.objects.get(docente=docente, periodo=periodo, asignatura=asignatura)
			horario = Horario.objects.get(asignatura=docasig, dia=datetime.datetime.now().weekday())
			fecha = datetime.datetime.now()
			dictado = form.save(commit=False)

			dictado.horario = horario
			dictado.fecha = fecha
			dictado.estado = 0  # Sin Revisa
			dictado.save()
			return render(request, 'planificacion/ingresar_dictado_correcto.html', {'dictado': dictado},
						  context_instance=RequestContext(request))

	else:
		if (Asignatura.objects.filter(codigo=asignatura).exists()):
			docente = request.user
			asignatura = Asignatura.objects.get(codigo=asignatura)
			periodo = Periodo.objects.get(estado=True)
			if (
			DocenteAsignaturaPeriodo.objects.filter(docente=docente, periodo=periodo, asignatura=asignatura).exists()):
				docasig = DocenteAsignaturaPeriodo.objects.get(docente=docente, periodo=periodo, asignatura=asignatura)
				if (Horario.objects.filter(asignatura=docasig, dia=datetime.datetime.now().weekday()).exists()):
					horario = Horario.objects.get(asignatura=docasig, dia=datetime.datetime.now().weekday())
					if not (Tema.objects.filter(fecha=datetime.datetime.now(), horario=horario).exists()):
						form = DictadoFormDocente()
						return render(request, 'planificacion/ingresa_dictado.html', {'form': form},
									  context_instance=RequestContext(request))
					else:
						error = 'La asignatura ' + asignatura.descripcion + ' ya cuenta con un tema registrado hoy'
				else:
					error = 'La asignatura ' + asignatura.descripcion + ' no registra horario para el dia de hoy'
			else:
				error = 'El docente ' + request.user.get_full_name() + ' no tiene registrada la asignatura ' + asignatura.descripcion
		else:
			raise Http404
	return render(request, 'planificacion/error_ingresar_dictado.html', {'error': error},
				  context_instance=RequestContext(request))


def ver_materia_reporte(request):
	docente = get_object_or_404(Docente, user_ptr=request.user)
	periodo = get_object_or_404(Periodo, estado=True)
	# asignatura = get_object_or_404(Asignatura, codigo = id)
	asignaturas = DocenteAsignaturaPeriodo.objects.filter(periodo=periodo, docente=docente)
	# asigEstudiante = DocenteAsignaturaPeriodoEstudiante.objects.filter(estudiante=estudiante)

	return render(request, 'docente/ver_asignaturas.html', {'asignaturas': asignaturas},
				  context_instance=RequestContext(request))


def ver_reporte_input_fechas(request, id):
	docente = get_object_or_404(Docente, user_ptr=request.user)
	asignatura = get_object_or_404(Asignatura, codigo=id)
	periodo = get_object_or_404(Periodo, estado=True)
	asigperiodo = DocenteAsignaturaPeriodo.objects.filter(asignatura=asignatura, periodo=periodo, docente=docente)
	# asigestudiante = DocenteAsignaturaPeriodoEstudiante.objects.filter(docenteasignatura__in=asigperiodo, estudiante = estudiante)
	horario = Horario.objects.filter(asignatura__in=asigperiodo)
	if request.method == 'POST':
		form = FechasReporte(request.POST)
		if form.is_valid():
			inicio = form['inicio'].value()
			fin = form['fin'].value()
			temas = Tema.objects.filter(horario__in=horario, fecha__range=(inicio, fin))
			return PDFTemplateResponse(request, "reportes/docente.html", {'temas': temas, 'asignatura': asignatura})
	else:
		form = FechasReporte()
	return render(request, 'estudiante/form_reporte.html', {'form': form}, context_instance=RequestContext(request))


@staff_member_required()
def coordinador_buscar_docentes(request):
	return render(request, 'docente/buscar.html', {}, context_instance=RequestContext(request))

@staff_member_required()
def coordinador_buscar_docentes_excel(request):
	return render(request, 'docente/buscar_excel.html', {}, context_instance=RequestContext(request))


def busqueda(request):
	if request.is_ajax():
		docente = Docente.objects.filter(first_name__startswith=request.GET['nombre'].upper()).values('first_name', 'last_name',
																							  'id') | Docente.objects.filter(
			last_name__startswith=request.GET['nombre'].upper()).values('first_name', 'last_name',
																'id') | Docente.objects.filter(
			cedula__startswith=request.GET['nombre']).values('first_name', 'last_name', 'id')
		return JsonResponse(list(docente), safe=False)
	else:
		return HttpResponse("Solo se permiten consultas mediante AJAX")

@staff_member_required()
def coordinador_reporte_materias(request, id):
	docente = get_object_or_404(Docente, user_ptr=id)
	periodo = get_object_or_404(Periodo, estado=True)
	# asignatura = get_object_or_404(Asignatura, codigo = id)
	asignaturas = DocenteAsignaturaPeriodo.objects.filter(periodo=periodo, docente=docente)
	# asigEstudiante = DocenteAsignaturaPeriodoEstudiante.objects.filter(estudiante=estudiante)
	lista = list()
	for i in asignaturas:
		lista.append(i.asignatura)
	return render(request, 'reportes/ver_asignaturas.html', {'asignaturas': asignaturas, 'docente': docente},
				  context_instance=RequestContext(request))

@staff_member_required()
def coordinador_reporte_materias_todo(request, id):
	docente = get_object_or_404(Docente, user_ptr=id)
	periodo = get_object_or_404(Periodo, estado=True)
	asignaturas = DocenteAsignaturaPeriodo.objects.filter(periodo=periodo, docente=docente)
	asignaturasClean = list()
	temasClean = list()
	for i in asignaturas:
		asignaturasClean.append(i.asignatura)
	horario = Horario.objects.filter(asignatura__in=asignaturas)
	temas = Tema.objects.filter(horario__in=horario, fecha__range=(periodo.fechainicio, periodo.fechafin))

	# return HttpResponse(temas)
	return PDFTemplateResponse(request, 'reportes/semestre_coordinador.html',
							   {'asignaturas': asignaturasClean, 'temas': temas, 'docente': docente})

class coordinador_reporte_materias_todo_xls(View):
	filename = 'excelfile.xlsx'

	def get(self, request, *args, **kwargs):
		data = Docente.objects.all()

		wb = xlsxwriter.Workbook(self.filename)

		sheet = wb.add_worksheet('sheet1')

		num_format = wb.add_format({
			'num_format': '0',
			'align': 'right',
			'font_size': 12,
		})

		general_format = wb.add_format({
			'align': 'left',
			'font_size': 12,
		})
		row = 8
		lista = list()
		for j in data:
			lista.append((j.cedula, j.first_name, j.last_name))
			row += 1
			sheet.write_row(row, 0, (j.cedula, j.first_name, j.last_name))

		wb.close()
		output = open(self.filename)
		response = HttpResponse(output, content_type="application/ms-excel")
		response['Content-Disposition'] = 'attachment; filename=Excel.xls'
		return response

	# return HttpResponse(open(self.filename).read(), content_type='application/ms-excel')

@staff_member_required()
def coordinador_asignaturas_xls(request, id):
	docente = get_object_or_404(Docente, user_ptr=id)
	periodo = get_object_or_404(Periodo, estado=True)
	asignaturas = DocenteAsignaturaPeriodo.objects.filter(periodo=periodo, docente=docente)
	asignaturasClean = list()
	temasClean = list()
	for i in asignaturas:
		asignaturasClean.append(i.asignatura)
	horario = Horario.objects.filter(asignatura__in=asignaturas)
	temas = Tema.objects.filter(horario__in=horario, fecha__range=(periodo.fechainicio, periodo.fechafin))

	return render(request, 'reportes/ver_asignaturas_xls.html', {'asignaturas': asignaturasClean},
				  context_instance=RequestContext(request))

@staff_member_required()
def coordinador_asignaturas_xls_asig(request, id, id2):
	docente = get_object_or_404(Docente, user_ptr=id)
	periodo = get_object_or_404(Periodo, estado=True)
	asignatura = get_object_or_404(Asignatura, codigo=id2)
	asignaturas = DocenteAsignaturaPeriodo.objects.filter(periodo=periodo, docente=docente, asignatura=asignatura)
	filename = docente.cedula + '-'+asignatura.codigo+'.xls'

	# return HttpResponse(temas)

	wb = xlsxwriter.Workbook(filename)

	reporte = wb.add_worksheet('sheet1')

	reporte.set_column(0, 0,30)
	reporte.set_column(1, 0, 30)
	reporte.set_column(2, 0, 30)
	#reporte.set_column(4, 0, 90)

	num_format = wb.add_format({
		'num_format': '0',
		'align': 'right',
		'font_size': 12,

	})

	formato_negrita = wb.add_format({
		'bold': True
	})

	general_format = wb.add_format({
		'align': 'left',
		'font_size': 12,
	})



	asignaturasClean = list()
	temasClean = list()
	for i in asignaturas:
		asignaturasClean.append(i.asignatura)
	horario = Horario.objects.filter(asignatura__in=asignaturas)
	temas = Tema.objects.filter(horario__in=horario, fecha__range=(periodo.fechainicio, periodo.fechafin))

	reporte.merge_range(0, 0, 0, 2, asignatura.descripcion)
	reporte.merge_range(1, 0, 1, 2, (docente.first_name + " " + docente.last_name))

	reporte.write(3, 0, "Tema", formato_negrita)
	reporte.write(3, 1, "Unidad", formato_negrita)
	reporte.write(3, 2, "Estado", formato_negrita)

	row = 3

	valores = {'0':0, '1': 0, '2':0}

	for tema in temas:
		row += 1
		reporte.write_row(row, 0, (tema.nombre, tema.unidad.nombre, tema.tema_string()))
		valores[tema.estado] = valores[tema.estado] + 1



	row = row + 3

	reporte.write(row, 0, "Estado", formato_negrita)
	reporte.write(row, 1, "Cantidad", formato_negrita)
	row += 1
	inicio = row

	reporte.write(row, 0 , "Sin Revisar")
	reporte.write(row, 1, valores['0'])
	row += 1
	reporte.write(row, 0, "Aprobados")
	reporte.write(row, 1, valores['1'])
	row += 1
	reporte.write(row, 0, "No Aprobados")
	reporte.write(row, 1, valores['2'])



	chart = wb.add_chart({'type': 'pie'})

	chart.title_name = 'Temas'

	chart.width = reporte._size_col(0)

	values = '=%s!%s' % (reporte.name, xl_range_abs(inicio,1,inicio+2,1))
	categories = '=%s!%s' % (reporte.name, xl_range_abs(inicio,0,inicio+2,0))
	chart.add_series({'values': values, 'categories': categories, 'smooth': True})

	reporte.insert_chart(inicio+4, 0, chart)


	wb.close()
	output = open(filename)
	nombre = 'attachment; filename='+filename
	response = HttpResponse(output, content_type="application/ms-excel")
	#response['Content-Disposition'] = 'attachment; filename=Excel.xls'
	response['Content-Disposition'] = nombre
	return response

@staff_member_required()
def horario_docente_buscar(request):
	return render(request, 'coordinador/buscar_horario.html', {}, context_instance=RequestContext(request))

@staff_member_required()
def horario_docente_lista(request, id):
	docente = get_object_or_404(Docente, user_ptr=id)
	periodo = get_object_or_404(Periodo, estado=True)
	asignaturasDocente = DocenteAsignaturaPeriodo.objects.filter(docente = docente, periodo = periodo).values('asignatura_id')
	asignaturas = Asignatura.objects.filter(id__in = asignaturasDocente)
	return render(request, 'coordinador/ver_asignaturas.html', {'asignaturas': asignaturas, 'docente':docente}, context_instance=RequestContext(request))

@staff_member_required()
def horario_docente_asignatura_horario(request, id_docente, id_asignatura):
	docente = get_object_or_404(Docente, user_ptr=id_docente)
	periodo = get_object_or_404(Periodo, estado=True)
	asignatura = get_object_or_404(Asignatura, codigo = id_asignatura)
	asignaturadocente = get_object_or_404(DocenteAsignaturaPeriodo, docente=docente,periodo=periodo,asignatura=asignatura)
	horarios = Horario.objects.filter(asignatura=asignaturadocente).order_by('dia')

	return render(request, 'coordinador/ver_horarios.html', {'horarios': horarios, 'asignatura':asignatura, 'docente':docente},
				  context_instance=RequestContext(request))

@staff_member_required()
def horario_docente_asignatura_horario_nuevo(request, id_docente, id_asignatura):
	periodo = get_object_or_404(Periodo, estado=True)
	asignatura = get_object_or_404(Asignatura, codigo=id_asignatura)
	docente = get_object_or_404(Docente, user_ptr=id_docente)
	docasigper = get_object_or_404(DocenteAsignaturaPeriodo, docente=docente, periodo=periodo, asignatura=asignatura)

	if request.method == 'POST':
		form = HorarioForm(request.POST)
		if form.is_valid():
			horario = form.save(commit=False)
			horario.asignatura = docasigper
			asignaturas = DocenteAsignaturaPeriodo.objects.filter(docente=docente, periodo=periodo)
			horarios = Horario.objects.filter(asignatura__in=asignaturas)

			for h in horarios:
				if h.inicio == horario.inicio:
					return render(request, 'coordinador/crear_horario.html',
								  {'form': form, 'asignatura': asignatura, 'docente': docente, 'error': True},
								  context_instance=RequestContext(request))

			try:
				horario.save()
				return HttpResponseRedirect(reverse('horario_docente_asignatura_horario', args=(id_docente,id_asignatura))+"?mensaje=correcto")
			except:
				return render(request, 'coordinador/crear_horario.html',
							  {'form': form, 'asignatura': asignatura, 'docente': docente, 'integridad': True},
							  context_instance=RequestContext(request))

	else:
		form = HorarioForm()
	return render(request, 'coordinador/crear_horario.html', {'form': form, 'asignatura': asignatura, 'docente':docente},
				  context_instance=RequestContext(request))



