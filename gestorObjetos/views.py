#encoding:utf-8
import os
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.core.files import File
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
import operator
from django.contrib import messages
from gestorObjetos.models import Repositorio, Objeto, Autor, RutaCategoria, EspecificacionLOM, PalabraClave
from gestorObjetos.forms import EspecificacionForm, cEspecificacionForm, ObjetosForm, cObjetosForm
import datetime
from filetransfers.api import serve_file
import siova.lib.Opciones as opc
import siova.lib.Archivos as mod_archivo

def ingresar(request):
	"""
		Vista que permite realizar el respectivo inicio de sesión para los Usuarios del sistema
	"""
	#Validación del usuario activo que ingresa a la página
	if not request.user.is_anonymous():
		#si es administrador se redirigirá a la interfaz de administración de lo contrario a la vista privado
		if request.user.profile.rol == "radm":
			return HttpResponseRedirect('/admin')
		else:
			return HttpResponseRedirect('/privado')
	#Si la petición a la vista ya contiene un objeto formulario diligenciado
	if request.method == 'POST':
		#Se instancia el formulario de autenticación por defecto de Django
		formulario = AuthenticationForm(request.POST)
		#Se valida el formualario en sus campos.
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					if request.user.profile.rol == "radm":
						return HttpResponseRedirect('/admin')
					else:
						return HttpResponseRedirect('/privado')
				else:
					return render_to_response('noactivo.html', context_instance=RequestContext(request))
			else:
				return render_to_response('nousuario.html', context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('ingresar.html', {'formulario':formulario}, context_instance = RequestContext(request))

def principal(request):
	"""
		Vista que muestra al usuario visitante la página inicial del sistema
	"""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/privado')
	else:
		repositorios = []
		if len(repositorios) == 0:
			repositorios = list(Repositorio.objects.filter(publico=True))
		else:
			repositorios.extend(list(Repositorio.objects.filter(publico=True)))
		repositorios = list(set(repositorios)) #quitar duplicados en la lista
		objetos = []
		for r in repositorios:
			if len(objetos) == 0:
				objetos = list(Objeto.objects.filter(repositorio=r).filter(publicado=True))
			else:
				objetos.extend(list(Objeto.objects.filter(repositorio=r).filter(publicado=True)))

		catn1 = RutaCategoria.objects.filter(cat_padre=None)
		catnTemp = list(RutaCategoria.objects.all().exclude(cat_padre=None))
		catn2=[]
		catn3=[]
		temp=0
		for c in catn1:
			for c1 in catnTemp:
				if c1.cat_padre == c:
					if c1 in catn2:
						temp=1 #variable temporal sin relevancia en la lógica
					else:
						catn2.append(c1)
		for d in catn2:
			for d1 in catnTemp:
				if d1.cat_padre == d:
					if d1 in catn3:
						temp=2 #variable temporal sin relevancia en la lógica
					else:
						catn3.append(d1)
		formulario=cEspecificacionForm
		return render_to_response('index.html',{'form':formulario, 'repos':repositorios, 'objetos':objetos, 'catn1':catn1, 'catn2':catn2, 'catn3':catn3},context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def privado(request):
	"""
	Vista que despliega la información dependiendo del usuario logueado en el sistema.
	"""
	repositorios = []
	for g in request.user.groups.all():
		repositorios.extend(list(Repositorio.objects.filter(grupos=g) | Repositorio.objects.filter(publico=True)))
	repositorios = list(set(repositorios)) #quitar duplicados en la lista
	objetos = []
	for r in repositorios:
		if len(objetos) == 0:
			objetos = list(Objeto.objects.filter(repositorio=r).filter(publicado=True))
		else:
			objetos.extend(list(Objeto.objects.filter(repositorio=r).filter(publicado=True)))

	catn1 = RutaCategoria.objects.filter(cat_padre=None)
	catnTemp = list(RutaCategoria.objects.all().exclude(cat_padre=None))
	catn2=[]
	catn3=[]
	temp=0
	for c in catn1:
		for c1 in catnTemp:
			if c1.cat_padre == c:
				if c1 in catn2:
					temp=1 #variable temporal sin relevancia en la lógica
				else:
					catn2.append(c1)
	for d in catn2:
		for d1 in catnTemp:
			if d1.cat_padre == d:
				if d1 in catn3:
					temp=2 #variable temporal sin relevancia en la lógica
				else:
					catn3.append(d1)
	formulario=cEspecificacionForm
	return render_to_response('privado.html',{'usuario':request.user, 'form':formulario, 'repos':repositorios, 'objetos':objetos, 'catn1':catn1, 'catn2':catn2, 'catn3':catn3},context_instance=RequestContext(request))

#@login_required(login_url='/ingresar')
def categoria(request, id_categoria):
	"""
	Vista que despliega las sub categorías y objetos pretenecientes a dicha catagoría.
	"""
	padre=None
	abuelo=None
	categoria = RutaCategoria.objects.get(pk=id_categoria)
	catn1 = list(RutaCategoria.objects.filter(cat_padre=categoria))
	padre = categoria.cat_padre
	if padre:
		abuelo = padre.cat_padre
	if request.user.is_authenticated():
		objetos = Objeto.objects.filter(ruta_categoria=categoria).filter(repositorio__grupos=request.user.groups.all()).filter(publicado=True) | Objeto.objects.filter(ruta_categoria=categoria).filter(repositorio__publico=True).filter(publicado=True)
		objetos = list(set(objetos)) #quitar duplicados en la lista
		data={'usuario':request.user, 'categoria':categoria, 'objetos':objetos, 'catn1':catn1, 'padre':padre, 'abuelo':abuelo}
	else:
		objetos = Objeto.objects.filter(ruta_categoria=categoria).filter(publicado=True).filter(repositorio__publico=True)
		data={'usuario':False,'categoria':categoria, 'objetos':objetos, 'catn1':catn1, 'padre':padre, 'abuelo':abuelo}
	return render_to_response('categoria.html',data,context_instance=RequestContext(request))

#@login_required(login_url='/ingresar')
def objeto(request, id_objeto):
	"""
	En esta vista se desplegarán la información del Objeto seleccionado
	"""
	obj=Objeto.objects.get(pk=id_objeto)
	gruposobj = obj.repositorio.grupos.all()
	gruposu = request.user.groups.all()
	puedever=False
	for go in gruposobj:
		for gu in gruposu:
			if go == gu:
				puedever=True
	if puedever | obj.repositorio.publico:
		idiom={}
		nivel_a={}
		format={}
		tipo_i={}
		nivel_i={}
		contex={}
		[idiom.update({k:v}) for k,v in opc.get_idiomas()]
		[nivel_a.update({k:v}) for k,v in opc.get_nivel_agregacion()]
		[format.update({k:v}) for k,v in opc.get_tipo_recurso()]
		[tipo_i.update({k:v}) for k,v in opc.get_tipo_interactividad()]
		[nivel_i.update({k:v}) for k,v in opc.get_nivel_interactividad()]
		[contex.update({k:v}) for k,v in opc.get_contexto()]
		if request.user.is_authenticated():
			data={'usuario':request.user, 'objeto':obj, 'espec':obj.espec_lom, 'autores':obj.autores.all(), 'keywords':obj.palabras_claves.all(),'idioma':idiom[obj.espec_lom.lc1_idioma],'niv_agr':nivel_a[obj.espec_lom.lc1_nivel_agregacion],'formato':format[obj.espec_lom.lc4_tipo_rec],'tipo_i':tipo_i[obj.espec_lom.lc4_tipo_inter],'nivel_i':nivel_i[obj.espec_lom.lc4_nivel_inter],'context':contex[obj.espec_lom.lc4_contexto]}
		else:
			data={'objeto':obj, 'espec':obj.espec_lom, 'autores':obj.autores.all(), 'keywords':obj.palabras_claves.all(),'idioma':idiom[obj.espec_lom.lc1_idioma],'niv_agr':nivel_a[obj.espec_lom.lc1_nivel_agregacion],'formato':format[obj.espec_lom.lc4_tipo_rec],'tipo_i':tipo_i[obj.espec_lom.lc4_tipo_inter],'nivel_i':nivel_i[obj.espec_lom.lc4_nivel_inter],'context':contex[obj.espec_lom.lc4_contexto]}
		return render_to_response('objeto.html',data,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def buscar(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		spec=[]
		r_obj=[]
		if request.user.is_authenticated():
			grupos = request.user.groups.all()
			for g in grupos:
				r_obj.extend(Objeto.objects.filter( Q( palabras_claves__palabra_clave__icontains = q ) | Q( espec_lom__lc1_titulo__icontains = q ) | Q( espec_lom__lc1_descripcion__icontains = q ) | Q( espec_lom__lc4_poblacion__icontains = q ) | Q( espec_lom__lc4_contexto__icontains = q ) | Q( espec_lom__lc6_uso_educativo__icontains = q )).order_by('espec_lom').filter(publicado=True).filter(repositorio__grupos=g))
		r_obj.extend(Objeto.objects.filter( Q( palabras_claves__palabra_clave__icontains = q ) | Q( espec_lom__lc1_titulo__icontains = q ) | Q( espec_lom__lc1_descripcion__icontains = q ) | Q( espec_lom__lc4_poblacion__icontains = q ) | Q( espec_lom__lc4_contexto__icontains = q ) | Q( espec_lom__lc6_uso_educativo__icontains = q )).order_by('espec_lom').filter(publicado=True).filter(repositorio__publico=True))
		rob=list(set(r_obj))
		for r in rob:
			spec.extend([r.espec_lom])
		d=rob+spec
		json_serializer = serializers.get_serializer("json")()
		data = json_serializer.serialize(d, ensure_ascii=False)
		return HttpResponse(data, mimetype='application/json')
	else:
		return render_to_response('privado.html', {'error': True},context_instance=RequestContext(request))

def busqueda(request):
	qlist = []
	if 'tit' in request.GET and request.GET['tit'] and request.GET['v_tit']=="True":
		titulo = request.GET['tit']
		qlist.append(('espec_lom__lc1_titulo__icontains',titulo))
	if 'tob' in request.GET and request.GET['tob'] and request.GET['v_tob']=="True":
		tipo = request.GET['tob']
		qlist.append(('tipo_obj__iexact',tipo))
	if 'idi' in request.GET and request.GET['idi'] and request.GET['v_idi']=="True":
		idioma = request.GET['idi']	
		qlist.append(('espec_lom__lc1_idioma__iexact',idioma))
	if 'nag' in request.GET and request.GET['nag'] and request.GET['v_nag']=="True":
		nivel_agregacion = request.GET['nag']	
		qlist.append(('espec_lom__lc1_nivel_agregacion__exact',nivel_agregacion))
	if 'fec' in request.GET and request.GET['fec'] and request.GET['v_fec']=="True":
		fech = request.GET['fec']
		fecha = datetime.datetime.strptime(fech,"%d/%m/%Y").strftime("%Y-%m-%d") 
		qlist.append(('espec_lom__lc2_fecha__lte',fecha))
	if 'tin' in request.GET and request.GET['tin'] and request.GET['v_tin']=="True":
		tipo_interactividad = request.GET['tin']	
		qlist.append(('espec_lom__lc4_tipo_inter__exact',tipo_interactividad))
	if 'tre' in request.GET and request.GET['tre'] and request.GET['v_tre']=="True":
		tipo_recurso = request.GET['tre']
		qlist.append(('espec_lom__lc4_tipo_rec__exact',tipo_recurso))
	if 'nin' in request.GET and request.GET['nin'] and request.GET['v_nin']=="True":
		nivel_interactividad = request.GET['nin']
		qlist.append(('espec_lom__lc4_nivel_inter__exact',nivel_interactividad))
	spec=[]
	q=[Q(x) for x in qlist]
	r_obj=[]
	if request.user.is_authenticated():
		grupos = request.user.groups.all()
		for g in grupos:
			r_obj.extend(Objeto.objects.filter(reduce(operator.and_, q)).filter(publicado=True).filter(repositorio__grupos=g))
	r_obj.extend(Objeto.objects.filter(reduce(operator.and_, q)).filter(publicado=True).filter(repositorio__publico=True))
	rob=list(set(r_obj))#Eliminar duplicados de la lista
	for r in rob:
		spec.extend([r.espec_lom])
	d=rob+spec
	json_serializer = serializers.get_serializer("json")()
	data = json_serializer.serialize(d, ensure_ascii=False)
	return HttpResponse(data, mimetype='application/json')

@login_required(login_url='/ingresar')
def docObjeto(request):
	"""
	Vista de acceso al usuario con rol de Docente, de esta manera se le permitirá crearobjetos
	"""
	if request.user.profile.rol == 'rdoc':
		objetos = Objeto.objects.filter(creador=request.user.id)
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
			formularioObj = ObjetosForm(gruposu, request.POST, request.FILES)
			if not error1:
				if formularioEsp.is_valid():#si es válido el formularo de especificaciónLOM
					if formularioObj.is_valid():#si el válido el objeto
						esp=formularioEsp.save()#se guarda la especificaciónLOM primero
						pc = formularioObj.cleaned_data['palabras_claves']#se toman las palabras claves digitadas
						re = formularioObj.cleaned_data['repositorio']#se toma el repositorio
						f=formularioObj.save(commit=False)#se guarda un instancia temporañ
						f.espec_lom = esp # se asocia el objeto con su especificaciónLOM
						f.creador=request.user # Se asocia el objeto con el usuario que lo crea
						f.repositorio=re
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
					else:
						errores=True
				else:
					errores = True
		else:
			formularioObj=ObjetosForm(gruposu)
			formularioEsp=EspecificacionForm()

		return render_to_response('docente.html',{'usuario':request.user,'objetos':objetos,'formObj':formularioObj,'formEsp':formularioEsp,'errores':errores,'l_errores':l_errores},context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

@login_required(login_url='/ingresar')
def editObjeto(request,id_objeto):
	"""
	Vista de acceso al usuario con rol de Docente, de esta manera se le permitirá modificar objetos
	"""
	obj=Objeto.objects.get(pk=id_objeto)#objeto que se está modificando
	kws=obj.palabras_claves.all()#palabras claves del objeto
	if request.user.profile.rol == 'rdoc':
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
				if not error1:
					if formularioEsp.is_valid() & formularioObj.is_valid():
						formularioEsp.save()
						pc = formularioObj.cleaned_data['palabras_claves']#se toman las palabras claves digitadas
						re = formularioObj.cleaned_data['repositorio']#se toma el repositorio
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
						f.save()
						#messages.add_message(request, messages.SUCCESS, 'Cambios Actualizados Exitosamente')# no funciona al redireccionar
						return HttpResponseRedirect('/objeto/'+str(obj.pk))
					else:
						errores=True
			else:
				formularioEsp = EspecificacionForm(instance=esp)
				formularioObj = cObjetosForm(request.user, obj, instance=obj)
			return render_to_response('editObjeto.html',{'objeto':obj,'usuario':request.user,'formObj':formularioObj,'formEsp':formularioEsp,'autores':autores,'errores':errores,'l_errores':l_errores},context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect('/')	
	else:
		return HttpResponseRedirect('/')


@login_required(login_url='/ingresar')
def crearAutor(request):
	"""
	Vista de acceso al usuario con rol de Docente, que le permite crear autores para los objetos.
	"""
	laut=[]
	if 'naut' in request.GET and request.GET['naut']:
		nombre = request.GET['naut']
	if 'aaut' in request.GET and request.GET['aaut']:
		apellido = request.GET['aaut']	
	if 'raut' in request.GET and request.GET['raut']:
		rol = request.GET['raut']
	else:
		rol="Autor"
	objAutor,creado=Autor.objects.get_or_create(nombres=nombre, apellidos=apellido, rol=rol)
	if creado: #Si ya existe el Autor se obvia el proceso de guardarlo en la bd
		objAutor.save() #se guarda el Autor en la bd
	laut.append(objAutor)
	json_serializer = serializers.get_serializer("json")()
	data = json_serializer.serialize(laut, ensure_ascii=False)
	return HttpResponse(data, mimetype='application/json')

"""
Vista que permite gestionar la descarga del objeto dependiendo de los permisos que tenga
"""
def download(request,id):
	f= get_object_or_404(Objeto, pk=id)
	gruposobj = f.repositorio.grupos.all()
	gruposu = request.user.groups.all()
	puededescargar=False
	for go in gruposobj:
		for gu in gruposu:
			if go == gu:
				puededescargar=True
	if request.user.is_authenticated():
		if puededescargar:
			return serve_file(request, f.archivo, save_as=f.espec_lom.lc1_titulo)
		elif f.repositorio.publico & f.publicado:
			return serve_file(request, f.archivo, save_as=f.espec_lom.lc1_titulo)
		else:
			return HttpResponseRedirect('/')
	elif f.repositorio.publico & f.publicado:
		return serve_file(request, f.archivo, save_as=f.espec_lom.lc1_titulo)
	else:
		return HttpResponseRedirect('/')

"""
Vista para la gestión de la descargar del objeto desde la interfaz de edición del mismo
"""
def downloadEdit(request, id):
	codigo_espec_archivo=int(id.split('.')[0].split('_')[1])#toma el id (nombre del archivo) y toma la parte que corresponde al pk del espec del archivo
	#f=Objeto.objects.get(archivo=miarchivo.file)
	f= get_object_or_404(Objeto, espec_lom=codigo_espec_archivo)
	gruposobj = f.repositorio.grupos.all()
	gruposu = request.user.groups.all()
	puededescargar=False
	for go in gruposobj:
		for gu in gruposu:
			if go == gu:
				puededescargar=True
	if request.user.is_authenticated():
		if puededescargar:
			return serve_file(request, f.archivo, save_as=f.espec_lom.lc1_titulo)
		elif f.repositorio.publico & f.publicado:
			return serve_file(request, f.archivo, save_as=f.espec_lom.lc1_titulo)
		else:
			return HttpResponseRedirect('/')
	elif f.repositorio.publico & f.publicado:
		return serve_file(request, f.archivo, save_as=f.espec_lom.lc1_titulo)
	else:
		return HttpResponseRedirect('/')

@login_required(login_url='/ingresar')
def cerrar(request):
	"""
	Vista que permite cerrar sesión de manera segura en el sistema.
	"""
	logout(request)
	return HttpResponseRedirect('/')

def redirige(request):
	"""
	Vista que permite redirigir hacia la página principal.
	"""
	return HttpResponseRedirect('/')