#encoding:utf-8
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from gestorObjetos.models import Repositorio, Objeto, Autor, RutaCategoria

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
	return render_to_response('privado.html',{'usuario':request.user, 'repos':repositorios, 'objetos':objetos, 'catn1':catn1, 'catn2':catn2, 'catn3':catn3},context_instance=RequestContext(request))

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
        r_obj = Objeto.objects.filter(espec_lom__lc1_titulo__icontains=q)
        return render_to_response('privado.html', {'resultado': r_obj, 'query': q})
    else:
        return render_to_response('privado.html', {'error': True})


@login_required(login_url='/ingresar')
def cerrar(request):
	"""
	Vista que permite cerrar sesión de manera segura en el sistema.
	"""
	logout(request)
	return HttpResponseRedirect('/')