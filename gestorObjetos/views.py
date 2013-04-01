#encoding:utf-8
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
import operator
from django.contrib import messages
from gestorObjetos.models import Repositorio, Objeto, Autor, RutaCategoria, EspecificacionLOM, PalabraClave
from gestorObjetos.forms import EspecificacionForm, cEspecificacionForm, ObjetosForm

def ingresar(request):
	"""
		Vista que permite realizar el respectivo inicio de sesión para los Usuarios del sistema
	"""
	if not request.user.is_anonymous():
		if request.user.profile.rol == "radm":
			return HttpResponseRedirect('/admin')
		else:
			return HttpResponseRedirect('/privado')
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
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

@login_required(login_url='/ingresar')
def privado(request):
	"""
	Vista que despliega la información dependiendo del usuario logueado en el sistema.
	"""
	repositorios = []
	for g in request.user.groups.all():
		if len(repositorios) == 0:
			repositorios = list(Repositorio.objects.filter(grupos=g))
		else:
			repositorios.extend(list(Repositorio.objects.filter(grupos=g)))
	repositorios = list(set(repositorios)) #quitar duplicados en la lista
	objetos = []
	for r in repositorios:
		if len(objetos) == 0:
			objetos = list(Objeto.objects.filter(repositorio=r))
		else:
			objetos.extend(list(Objeto.objects.filter(repositorio=r)))

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
	formulario=EspecificacionForm
	return render_to_response('privado.html',{'usuario':request.user, 'form':formulario, 'repos':repositorios, 'objetos':objetos, 'catn1':catn1, 'catn2':catn2, 'catn3':catn3},context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def categoria(request, id_categoria):
	"""
	Vista que despliega las sub categorías y objetos pretenecientes a dicha catagoría.
	"""
	categoria = RutaCategoria.objects.get(pk=id_categoria)
	catn1 = list(RutaCategoria.objects.filter(cat_padre=categoria))
	objetos = categoria.objeto_set.all()
	return render_to_response('categoria.html',{'usuario':request.user, 'categoria':categoria, 'objetos':objetos, 'catn1':catn1},context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def objeto(request, id_objeto):
	"""
	En esta vista se desplegarán la información del Objeto seleccionado
	"""
	obj=Objeto.objects.get(pk=id_objeto)
	return render_to_response('objeto.html',{'usuario':request.user, 'objeto':obj, 'espec':obj.espec_lom, 'autores':obj.autores.all(), 'keywords':obj.palabras_claves.all()},context_instance=RequestContext(request))

def buscar(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		spec=[]
		r_obj = list(Objeto.objects.filter( Q( palabras_claves__palabra_clave__icontains = q ) | Q( espec_lom__lc1_titulo__icontains = q ) | Q( espec_lom__lc1_descripcion__icontains = q ) | Q( espec_lom__lc4_poblacion__icontains = q ) | Q( espec_lom__lc4_contexto__icontains = q ) | Q( espec_lom__lc6_uso_educativo__icontains = q )).order_by( 'espec_lom'))
		rob=list(set(r_obj))
		for r in rob:
			spec.extend(list(EspecificacionLOM.objects.filter(pk=r.id)))
		d=rob+spec
		json_serializer = serializers.get_serializer("json")()
		data = json_serializer.serialize(d, ensure_ascii=False)
		return HttpResponse(data, mimetype='application/json')
	else:
		return render_to_response('privado.html', {'error': True},context_instance=RequestContext(request))

def busqueda(request):
	qlist = []
	if 'tit' in request.GET and request.GET['tit']:
		titulo = request.GET['tit']
		qlist.append(('espec_lom__lc1_titulo__iexact',titulo))
	if 'idi' in request.GET and request.GET['idi']:
		idioma = request.GET['idi']	
		qlist.append(('espec_lom__lc1_idioma__iexact',idioma))
	if 'nag' in request.GET and request.GET['nag']:
		nivel_agregacion = request.GET['nag']	
		qlist.append(('espec_lom__lc1_nivel_agregacion__exact',nivel_agregacion))
	if 'fec' in request.GET and request.GET['fec']:
		fecha = request.GET['fec']	
		qlist.append(('espec_lom__lc2_fecha__exact',fecha))
	if 'tin' in request.GET and request.GET['tin']:
		tipo_interactividad = request.GET['tin']	
		qlist.append(('espec_lom__lc4_tipo_inter__exact',tipo_interactividad))
	if 'tre' in request.GET and request.GET['tre']:
		tipo_recurso = request.GET['tre']	
		qlist.append(('espec_lom__lc4_tipo_rec__exact',tipo_recurso))
	if 'nin' in request.GET and request.GET['nin']:
		nivel_interactividad = request.GET['nin']
		qlist.append(('espec_lom__lc4_nivel_inter__exact',nivel_interactividad))
	spec=[]
	q=[Q(x) for x in qlist]
	r_obj = list(Objeto.objects.filter(reduce(operator.and_, q)))
	rob=list(set(r_obj))#Eliminar duplicados de la lista
	for r in rob:
		spec.extend(list(EspecificacionLOM.objects.filter(pk=r.id)))
	d=rob+spec
	json_serializer = serializers.get_serializer("json")()
	data = json_serializer.serialize(d, ensure_ascii=False)
	return HttpResponse(data, mimetype='application/json')

@login_required(login_url='/ingresar')
def docObjeto(request):
	"""
	Vista de acceso al usuario con rol de Docente, de esta manera se le permitirá crear/modificar/eliminar objetos
	"""
	errores = False
	if request.method == 'POST':
		formularioEsp = cEspecificacionForm(request.POST)
		formularioObj = ObjetosForm(request.POST, request.FILES)
		if formularioEsp.is_valid():#si es válido el formularo de especificaciónLOM
			esp=formularioEsp.save()#se guarda la especificaciónLOM primero
			if formularioObj.is_valid():#si el válido el objeto
				pc = formularioObj.cleaned_data['palabras_claves']#se toman las palabras claves digitadas
				f=formularioObj.save(commit=False)#se guarda un instancia temporañ
				f.espec_lom = esp # se asocia el objeto con su especificaciónLOM
				f.creador=request.user # Se asocia el objeto con el usuario que lo crea
				f.save() # se guarda el objeto en la base de datos.
				if ',' in pc: #si hay comas en las palabras claves
					lpc=[x.strip() for x in pc.split(',')] # se utilizan las palabras claves como una lista de palabras separadas sin comas ni espacios
				else:
					lpc=[x.strip() for x in pc.split()] # se utilizan las palabras claves como una lista de palabras separadas sin espacios
				for l in lpc:
					p,b=PalabraClave.objects.get_or_create(palabra_clave=l) # Se crea una palabra clave por cada palabra en la lista
					if not b: #Si ya existe la palabra entonces se obvia el proceso de crearla
						p.save() #se guarda la palabra clave en la bd
					f.palabras_claves.add(p) # se añade cada palabra clave al objeto
				messages.add_message(request, messages.SUCCESS, 'Objeto Agregado Exitosamente')
				formularioObj=ObjetosForm()
				formularioEsp=cEspecificacionForm()
			else:
				errores=True
		else:
			errores = True
	else:
		formularioObj=ObjetosForm()
		formularioEsp=cEspecificacionForm()
	objetos = Objeto.objects.filter(creador=request.user.id)

	return render_to_response('docente.html',{'usuario':request.user,'objetos':objetos,'formObj':formularioObj,'formEsp':formularioEsp,'errores':errores},context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def cerrar(request):
	"""
	Vista que permite cerrar sesión de manera segura en el sistema.
	"""
	logout(request)
	return HttpResponseRedirect('/')