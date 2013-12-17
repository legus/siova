#encoding:utf-8
from gestorProyectos.models import Proyecto, Facultad, Programa, Validacion, Parametro, Indicador
from gestorObjetos.models import Autor, Repositorio, Objeto, Autor, RutaCategoria, EspecificacionLOM, PalabraClave
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import siova.lib.Opciones as opc
from django.contrib.auth.decorators import login_required
from django.core import serializers

@login_required(login_url='/ingresar')
def verProyectos(request):
	proyectos= Proyecto.objects.exclude(fase='f1').order_by('fase')
	repositorios = []
	objetos = []
	return render_to_response('revisor.html', {'usuario':request.user, 'proyectos':proyectos}, context_instance=RequestContext(request))

def ver_proyecto(request):
	pro=[]
	met=[]
	aut=[]
	q = request.GET['q']
	obj=Objeto.objects.filter(proyecto=q)
	#Proyecto.objects.filter(pk=o.proyecto.pk)
	aut.extend(Autor.objects.filter(objeto__proyecto=q))
	for o in obj:
		met.extend(EspecificacionLOM.objects.filter(pk=o.espec_lom.pk))
		pro.extend(Programa.objects.filter(pk=o.proyecto.programa.pk))
	met2=list(set(met))
	pro2=list(set(pro))
	au2=list(set(aut))
	d=met2+pro2+au2
	json_serializer = serializers.get_serializer("json")()
	data = json_serializer.serialize(d, ensure_ascii=False)
	return HttpResponse(data, mimetype='application/json')