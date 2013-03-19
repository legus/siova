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
from gestorObjetos.models import Repositorio

def ingresar(request):
	"""
		Vista que permite realizar el respectivo inicio de sesión para los Usuarios del sistema
	"""
	if not request.user.is_anonymous():
		if request.user.rol == "radm":
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
					if request.user.rol == "radm":
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
	usuario = request.user
	repositorios = Repositorio.objects.all()
	return render_to_response('privado.html',{'usuario':usuario, 'repo':repositorios},context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def cerrar(request):
	"""
	Vista que permite cerrar sesión de manera segura.
	"""
	logout(request)
	return HttpResponseRedirect('/')