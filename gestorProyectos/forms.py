#encoding:utf-8
from django.forms import ModelForm, Textarea, TextInput
from django import forms
import datetime
from django.contrib.admin.widgets import AdminFileWidget
#from django.forms.widgets import ClearableFileInput
from gestorObjetos.models import EspecificacionLOM, Objeto, Repositorio, PalabraClave
from gestorProyectos.models import Proyecto, Programa, Facultad
import siova.lib.Opciones as opc
"""
Formulario basado en el modelo Proyecto
"""
class ProyectoForm(ModelForm):
	class Meta:
		model=Proyecto
		#modificación de cada uno de los campos que se muestran en la plantilla para que tengan un tamaño fijo
		exclude = ('titulo','fase','parametros','calificacion','indicadores','operaciones','nota')
	fecha = forms.DateField(initial=datetime.date.today, label="Fecha", help_text='Fecha en que el proyecto fue Aprobado')