#encoding:utf-8
from gestorProyectos.models import Proyecto, Facultad, Programa, Factor_competencias, Indicador, Enunciado, OperacionMental
from django.shortcuts import render_to_response
from gestorObjetos.models import Repositorio, Objeto, Autor, RutaCategoria, EspecificacionLOM, PalabraClave
from gestorProyectos.forms import ProyectoForm
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from gestorObjetos.forms import EspecificacionForm, cEspecificacionForm, ObjetosForm, cObjetosForm
from django.contrib import messages
import siova.lib.Opciones as opc
from django.contrib.auth.decorators import login_required
from decimal import Decimal

def Proyecto(request):
	"""
	Vista de acceso al usuario con rol de Catalogador, de esta manera se le permitirá crearProyectos	
	"""
	if request.user.profile.rol == 'rcat':
		proyectoObj= Objeto.objects.filter(proyecto__isnull=False)		
		gruposu = request.user.groups.all()
		errores = False
		error1 = False
		l_errores=[]
		if request.method == 'POST':
			if not request.POST.get('autores1'):
				l_errores.append('No incluyó autores al objeto.')
				error1=True
			if not request.POST.get('palabras_claves'):
				l_errores.append('No incluyó palabras claves al objeto.')
				error1=True
			if not request.POST.get('repositorio'):
				l_errores.append('No seleccionó repositorio. Si no hay repositorios asociados, consulte a un administrador del sistema para agregar alguno.')
				error1=True
			l_autores = request.POST.getlist('autores1')
			formularioEsp = EspecificacionForm(request.POST)
			formularioPro = ProyectoForm(request.POST)
			formularioObj = ObjetosForm(gruposu, request.POST, request.FILES)
			if not error1:
				if formularioEsp.is_valid():
					if formularioObj.is_valid():#si el válido el objeto
						if formularioPro.is_valid():#si el válido el proyecto
							esp=formularioEsp.save()#se guarda la especificaciónLOM primero
							pc = formularioObj.cleaned_data['palabras_claves']#se toman las palabras claves digitadas
							re = formularioObj.cleaned_data['repositorio']#se toma el repositorio
							pro=formularioPro.save(commit=False)#se guarda una instancia temporal
							ti = formularioEsp.cleaned_data['lc1_titulo']
							pro.titulo = ti #se asocia el proyecto con su titulo
							pro.nota=Decimal('0.0')
							pro.save()
							f=formularioObj.save(commit=False)#se guarda un instancia temporañ
							f.espec_lom = esp # se asocia el objeto con su especificaciónLOM
							f.creador=request.user # Se asocia el objeto con el usuario que lo crea
							f.repositorio=re # se asoicia el objeto con su repositorio
							f.proyecto=pro #se asocia el proyecto con el usuario que lo crea
							f.save() # se guarda el objeto en la base de datos.	
							if ',' in pc: #si hay comas en las palabras claves
								lpc=[x.strip() for x in pc.split(',')] # se utilizan las palabras claves como una lista de palabras separadas sin comas ni espacios
							else:
								lpc=[x.strip() for x in pc.split(' ')] # se utilizan las palabras claves como una lista de palabras separadas sin espacios
							for l in lpc:
								p,b=PalabraClave.objects.get_or_create(palabra_clave=l) # Se crea una palabra clave por cada palabra en la lista
								if not b: #Si ya existe la palabra entonces se obvia el proceso de crearla
									p.save() #se guarda la palabra clave en la bd
								f.palabras_claves.add(p) # se añade cada palabra clave al objeto
							for l in l_autores: #como el objeto llega como una lista... se debe recorrer per en realidad siempre tiene un solo objeto
								stri=l.split(',') #se divide la lista por comas que representa cada string de campos del autor
								for st in stri: # se recorre cada autor
									s=st.split(' ') # se divide los campos nombres, apellidos y rol en una lista
									aut,cr=Autor.objects.get_or_create(nombres=s[0].replace('-',' '), apellidos=s[1].replace('-',' '), rol=s[2].replace('-',' '))
									if not cr: #Si ya existe el autor entonces se obvia el proceso de crearlo
										aut.save() #se guarda el autor en la bd
									f.autores.add(aut) # se añade al campo manytomany con Autores.
							messages.add_message(request, messages.SUCCESS, 'Objeto Agregado Exitosamente')
							formularioObj=ObjetosForm(gruposu)
							formularioEsp=EspecificacionForm()
							formularioPro=ProyectoForm()
						else:
							errores=True
					else:
						errores = True	
				else:
					errores = True						
		else:
			formularioObj=ObjetosForm(gruposu)
			formularioEsp=EspecificacionForm()
			formularioPro=ProyectoForm()

		return render_to_response('proyecto.html', {'usuario':request.user, 'proyecto':proyectoObj, 'formObj':formularioObj, 'formPro':formularioPro, 'formEsp':formularioEsp,'errores':errores,'l_errores':l_errores}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def verProyecto(request, id_proyecto):
	"""
	En esta vista se desplegarán la información del Proyecto seleccionado
	"""
	obj=Objeto.objects.get(pk=id_proyecto)
	#Se consultan los indicadores asociados al proyecto
	l_indicadores = obj.proyecto.indicadores.all().order_by('factor')
	l_operaciones = obj.proyecto.operaciones.all()
	gruposobj = obj.repositorio.grupos.all()
	gruposu = request.user.groups.all()
	puedever=False
	for go in gruposobj:
		for gu in gruposu:
			if go == gu:
				puedever=True
	if puedever | obj.repositorio.publico:
		if request.user.is_authenticated():
			data={'usuario':request.user, 'objeto':obj, 'espec':obj.espec_lom, 'autores':obj.autores.all(), 'keywords':obj.palabras_claves.all(), 'proyecto':obj.proyecto,'indicadores':l_indicadores,'operaciones':l_operaciones}
		else:
			data={'objeto':obj, 'espec':obj.espec_lom, 'autores':obj.autores.all(), 'keywords':obj.palabras_claves.all(),'proyecto':obj.proyecto,'indicadores':l_indicadores}
		return render_to_response('verProyecto.html',data,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

@login_required(login_url='/ingresar')
def editProyecto(request,id_objeto):
	"""
	Vista de acceso al usuario con rol de Catalogador, de esta manera se le permitirá modificar objetos
	"""
	obj=Objeto.objects.get(pk=id_objeto)#objeto que se está modificando
	pro=obj.proyecto
	kws=obj.palabras_claves.all()#palabras claves del objeto
	if request.user.profile.rol == 'rcat':
		if obj.creador == request.user:
			error1 = False
			errores = False
			l_errores=[]
			gruposu = request.user.groups.all()
			esp=obj.espec_lom
			l_autores = request.POST.getlist('autores1')
			autores = obj.autores.all()
			lista_autores=[]#lista para guardar los autores incluidos en el formulario, ya sea para añadir o eliminar.
			lista_temporal=[]#lista temporal con los datos de los autores sin el caracter - para guardar los autores incluidos en el formulario, ya sea para añadir o eliminar.
			if request.method == 'POST':
				if not request.POST.getlist('autores1'):
					l_errores.append('No incluyó autores al objeto.')
					error1=True
				if len(l_autores[0])==0:
					l_errores.append('No incluyó autores al objeto.')
					error1=True
				if not request.POST.get('palabras_claves'):
					l_errores.append('No incluyó palabras claves al objeto.')
					error1=True
				formularioEsp = EspecificacionForm(request.POST, instance=esp)
				formularioObj = cObjetosForm(request.user, obj, request.POST, request.FILES, instance=obj)
				formularioPro = ProyectoForm(request.POST, instance=pro)
				if not error1:
					if formularioEsp.is_valid() & formularioObj.is_valid() & formularioPro.is_valid():
						formularioEsp.save()
						pc = formularioObj.cleaned_data['palabras_claves']#se toman las palabras claves digitadas
						re = formularioObj.cleaned_data['repositorio']#se toma el repositorio
						pro=formularioPro.save(commit=False)#se guarda una instancia temporal
						ti = formularioEsp.cleaned_data['lc1_titulo']
						pro.titulo = ti #se asocia el proyecto con su titulo 
						pro.save()
						f=formularioObj.save(commit=False)#se guarda un instancia temporal
						lpc=[x.strip() for x in pc.split(' ')] # se utilizan las palabras claves como una lista de palabras separadas sin espacios
						for l in lpc:
							p,b=PalabraClave.objects.get_or_create(palabra_clave=l) # Se crea una palabra clave por cada palabra en la lista
							if not b: #Si ya existe la palabra entonces se obvia el proceso de crearla
								p.save() #se guarda la palabra clave en la bd
							f.palabras_claves.add(p) # se añade cada palabra clave al objeto
						for kw in kws: #Se recorre todo el conjunto de palabras claves del objeto
							if kw.palabra_clave not in lpc: #se valida si cada palabra clave todavía se mantiene en lo que el usuario digitó
								f.palabras_claves.remove(kw) #de no encontrarse la palabra clave debe desasociarse aunque no eliminarse.
						for l in l_autores: #como el objeto llega como una lista... se debe recorrer per en realidad siempre tiene un solo objeto
							lista_autores=l.split(',') #se divide la lista por comas que representa cada string de campos del autor
							for st in lista_autores: # se recorre cada autor
								lista_temporal.append(st.replace('-',' '))
								s=st.split(' ') # se divide los campos nombres, apellidos y rol en una lista
								aut,cr=Autor.objects.get_or_create(nombres=s[0].replace('-',' '), apellidos=s[1].replace('-',' '), rol=s[2].replace('-',' '))
								if not cr: #Si ya existe el autor entonces se obvia el proceso de crearlo
									aut.save() #se guarda el autor en la bd
								f.autores.add(aut) # se añade al campo manytomany con Autores.
						for autor in autores: #Se recorre todo el conjunto de autores del objeto
							cadena_temporal=autor.nombres+' '+autor.apellidos+' '+autor.rol #cadena que concatena los datos del autor para compararlos con la lista que el usuario digita
							if cadena_temporal not in lista_temporal: #se valida si cada autor todavía se mantiene en lo que el usuario digitó
								f.autores.remove(autor) #de no encontrarse el autor, debe desasociarse aunque no eliminarse.
						f.repositorio=re
						f.proyecto=pro
						f.save()
						#messages.add_message(request, messages.SUCCESS, 'Cambios Actualizados Exitosamente')# no funciona al redireccionar
						return HttpResponseRedirect('/proyecto/'+str(obj.pk))
					else:
						errores=True
			else:
				formularioEsp = EspecificacionForm(instance=esp)
				formularioObj = cObjetosForm(request.user, obj, instance=obj)
				formularioPro = ProyectoForm(instance=pro)
			return render_to_response('editProyecto.html',{'objeto':obj, 'usuario':request.user,'formObj':formularioObj,'formEsp':formularioEsp,'formPro':formularioPro, 'proyecto':obj.proyecto, 'autores':autores,'errores':errores,'l_errores':l_errores},context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect('/')	
	else:
		return HttpResponseRedirect('/')

@login_required(login_url='/ingresar')
def asociarProyecto(request,id_objeto):
	"""
	Vista de acceso al usuario con rol de Catalogador, de esta manera se le permitirá asociar y modificar proyectos
	"""
	if request.user.profile.rol == 'rcat':
		obj = Objeto.objects.get(pk=id_objeto)#objeto que se está asociando
		fac = Factor_competencias.objects.filter(ruta_categoria=obj.ruta_categoria)
		operaciones=OperacionMental.objects.all()
		#Se consultan los indicadores asociados al proyecto
		#l_indicadores_previa = obj.proyecto.indicadores.all().order_by('factor')
		lindicadores = []
		lenunciado = []
		l_errores = []
		pro=obj.proyecto #instancia del proyecto asociado
		l_oind=pro.indicadores.all()
		operaciones2=pro.operaciones.all()
		error = False
		if pro.fase=='f3':
			l_errores.append("El proyecto no puede ser asociado a estándares de competencia debido a que ya ha sido valorado")
			error=True
		else:
			for f in fac:
				if len(lenunciado) == 0:
					lenunciado = list(Enunciado.objects.filter(factor=f))
				else:
					lenunciado.extend(list(Enunciado.objects.filter(factor=f)))
			if len(lenunciado) > 0:
				for e in lenunciado:
					if len(lindicadores) == 0:
						lindicadores = list(Indicador.objects.filter(enunciado=e))
					else:
						lindicadores.extend(list(Indicador.objects.filter(enunciado=e)))
			else:
				for f in fac:
					if len(lindicadores) == 0:
						lindicadores = list(Indicador.objects.filter(factor=f))
					else:
						lindicadores.extend(list(Indicador.objects.filter(factor=f)))
		if request.method == 'POST':
			errores = False
			error2 = False
			error3 = False
			gruposu = request.user.groups.all()
			l_indicadores = request.POST.iteritems()
			for key, value in l_indicadores:
				if key.find('ind_')>=0:
					error2=True
				if key.find('op_')>=0:
					error3=True
			if error2 and error3: #Quiere decir que se eligieron tanto indicadores como operaciones mentales
				l_indicadores = request.POST.iteritems()
				for key, value in l_indicadores:
					if key.find('ind_')>=0:
						i = Indicador.objects.get(pk=value)
						if i not in l_oind:
							pro.indicadores.add(i)
					if key.find('op_')>=0:
						operacion = OperacionMental.objects.get(pk=value)
						if operacion not in operaciones2:
							pro.operaciones.add(operacion)

				for o in l_oind:
					l_indicadores_temp = request.POST.iteritems()
					temp=""
					for k, v in l_indicadores_temp:
						if k.find('ind_')>=0:
							temp=temp+k.lstrip('ind_')
					if str(o.pk) not in temp:
						pro.indicadores.remove(o)
				
				for op in operaciones2:
					l_indicadores_temp = request.POST.iteritems()
					temp=""
					for k, v in l_indicadores_temp:
						if k.find('op_')>=0:
							temp=temp+k.lstrip('op_')
					if str(op.pk) not in temp:
						pro.operaciones.remove(op)
				pro.fase='f2'
				pro.save()
				return HttpResponseRedirect('/proyecto/'+str(obj.pk))
			elif error2:
				l_errores.append("No es posible asociar indicadores sin al menos una operación mental")
			elif error3:
				l_errores.append("No asoció ningún indicador al proyecto")
			else:
				pro.fase='f1'
				for p3 in pro.indicadores.all():
					pro.indicadores.remove(p3)
				for o3 in pro.operaciones.all():
					pro.operaciones.remove(o3)
				pro.save()
				return HttpResponseRedirect('/proyecto/'+str(obj.pk))
		l_oind=pro.indicadores.all()
		operaciones2=pro.operaciones.all()
		data={'usuario':request.user,'objeto':obj,'proyecto':pro,'espec':obj.espec_lom,'operaciones':operaciones,'operaciones2':operaciones2,'autores':obj.autores.all(),'keywords':obj.palabras_claves.all(),'l_oind':l_oind,'l_errores':l_errores,'factor':fac,'lenunciado':lenunciado,'lindicadores':lindicadores}
		return render_to_response('asociarProyecto.html',data,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')