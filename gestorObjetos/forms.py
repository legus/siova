#encoding:utf-8
from django.forms import ModelForm
from django import forms
from gestorObjetos.models import EspecificacionLOM

class EspecificacionForm(ModelForm):
	class Meta:
		model=EspecificacionLOM