#encoding:utf-8
from django.forms import ModelForm, Textarea, TextInput
from django import forms
import datetime
from gestorProyectos.models import Parametro, Validacion
import siova.lib.Opciones as opc

"""
Formulario basado en el modelo Parámetro para la respectiva validación del proyecto
"""
class ValidarForm(ModelForm):
	class Meta:
		model=Validacion
		#modificación de cada uno de los campos que se muestran en la plantilla para que tengan un tamaño fijo
		exclude=('proyecto')
		widgets = {
			'observaciones': Textarea(attrs={'cols': 40, 'rows': 2}),
			'valoracion': forms.RadioSelect(),
			'parametro':forms.HiddenInput()
		}