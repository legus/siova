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
from gestorObjetos.models import Repositorio, Objeto, Autor

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
	objetos = []
	for r in repositorios:
		if len(objetos) == 0:
			objetos = list(Objeto.objects.filter(repositorio=r))
		else:
			objetos.extend(list(Objeto.objects.filter(repositorio=r)))

	return render_to_response('privado.html',{'usuario':request.user, 'repos':repositorios, 'objetos':objetos},context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def objeto(request, id_objeto):
	"""
	En esta vista se desplegarán la información del Objeto seleccionado
	"""
	obj=Objeto.objects.get(pk=id_objeto)
	return render_to_response('objeto.html',{'usuario':request.user, 'objeto':obj, 'espec':obj.espec_lom, 'autores':obj.espec_lom.autores.all(), 'keywords':obj.espec_lom.palabras_claves.all()},context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def cerrar(request):
	"""
	Vista que permite cerrar sesión de manera segura en el sistema.
	"""
	logout(request)
	return HttpResponseRedirect('/')