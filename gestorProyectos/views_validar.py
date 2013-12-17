#encoding:utf-8
from gestorProyectos.models import Proyecto, Facultad, Programa, Validacion, Parametro, Indicador
from gestorObjetos.models import Repositorio, Objeto, Autor, RutaCategoria, EspecificacionLOM, PalabraClave
from gestorProyectos.forms import ProyectoForm
from gestorProyectos.formValidar import ValidarForm
from gestorObjetos.forms import EspecificacionForm, cEspecificacionForm, ObjetosForm, cObjetosForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import siova.lib.Opciones as opc
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.forms import Textarea
from decimal import Decimal

@login_required(login_url='/ingresar')
def validar(request, id_proyecto):
	"""
	En esta vista se implementará la lógica para la validación de proyectos
	"""
	obj=Objeto.objects.get(proyecto=id_proyecto)
	gruposu = request.user.groups.all()
	gruposobj = obj.repositorio.grupos.all()
	puederevisar=False
	#Se valida si el proyecto/objeto a revisar está en el mismo grupo que el usuario que va a revisar
	for go in gruposobj:
		for gu in gruposu:
			if go == gu:
				puederevisar=True
	#Si el usuario está en el mismo grupo del proyecto/objeto
	if puederevisar:
		#Si el perfil del usuario es el de revisor Y si el proyecto no está en fase 1
		if request.user.profile.rol == 'rrev' and obj.proyecto.fase != "f1":#
			errores = False
			l_errores=[]
			tipos={}
			calif=0
			l_valores_iniciales=[]
			l_valoraciones=[]#En caso de que la nota ya haya sido dada se necesitará guardar las nuevas notas para recalcular
			num_p=0
			#Se consultan los indicadores asociados al proyecto
			l_indicadores = obj.proyecto.indicadores.all().order_by('factor')
			#Se consultan las operaciones mentales asciadas al proyecto
			l_operaciones = obj.proyecto.operaciones.all()
			#Se consultan los paramétros y validaciones
			parametros=Parametro.objects.all().order_by('tipo', '-ponderacion')
			check=Validacion.objects.filter(proyecto=obj.proyecto.pk)
			#Se llena la lista de tipos por aparte
			[tipos.update({k:v}) for k,v in opc.get_tipo_p()]
			#se verifica si el proyecto ya tiene validaciones con el fin de crear o modificar la calificación
			if check.count()>0:
				consulta=check
				num_p=0
			else:
				consulta=Validacion.objects.none()
				num_p=parametros.count()
			#El set de formularios debe inicializarse con un número de formularios que dependen de si está creando o editando
			formularioValidar = modelformset_factory(Validacion, extra=num_p, form=ValidarForm)
			
			if request.method == 'POST':
				f_validar=formularioValidar(request.POST)
				#Verifico todos los datos enviados por formulario para validar si no se ha ingresado alguna calificacion
				#En caso de faltar alguna calificación, se debe devolver.
				for key, value in request.POST.iteritems():
					if key.find('form') >= 0:
						if key.find('valoracion') > 0:
							if value == '0.0':
								errores=True
								l_errores.append(key)
				#Si no hubieron errores y todos los parámetros fueron calificados
				if not errores:
					if f_validar.is_valid():
						instances=f_validar.save(commit=False)
						#Se recorre los datos del formulario para reemplazar los valores ocultos (proyecto y parámetro)
						for index, form in enumerate(instances):
							form.proyecto=obj.proyecto
							form.parametro=parametros[index]

						f_validar.save()
						#Si la nota se debe actualizar porque ya estaba calificado
						validaciones=Validacion.objects.filter(proyecto=obj.proyecto.pk)
						for v in validaciones:
							#se saca el parámetro de cada validación
							par=Parametro.objects.get(id=v.parametro.pk)
							#La calificación es la sumatoria de la multiplicación de la valoración y la ponderación de cada parámetro.
							calif=calif+(Decimal(v.valoracion)*par.ponderacion)
						#Si la calificación supera el umbral para la calificación
						if calif >= opc.get_umbral_calificacion():
							obj.proyecto.calificacion='a'
						else:
							obj.proyecto.calificacion='r'
						#Se actualiza la fase del proyecto
						obj.proyecto.fase='f3'
						#Se actualiza la nota del proyecto
						obj.proyecto.nota=calif
						obj.proyecto.save()
						return HttpResponseRedirect('/proyecto/'+str(obj.pk))
			else:
				#Los valores iniciales del formaulario son los campos ocultos (proyecto y parámetro)
				for p in parametros:
					l_valores_iniciales.append({'proyecto':obj.proyecto.pk, 'parametro':p})
				#Se sobreescribe el set de formaularios antes de enviar para que tenga los valores iniciales
				f_validar = formularioValidar(queryset=consulta, initial=l_valores_iniciales)
			data={'errores':l_errores, 'indicadores':l_indicadores, 'operaciones':l_operaciones, 'tipos':tipos, 'parametros':parametros, 'formValidar':f_validar, 'usuario':request.user, 'objeto':obj, 'espec':obj.espec_lom, 'autores':obj.autores.all(), 'keywords':obj.palabras_claves.all(), 'proyecto':obj.proyecto}
			return render_to_response('validar.html',data,context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/')