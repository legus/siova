#encoding:utf-8
from django.forms import ModelForm
from django import forms
import datetime
from gestorObjetos.models import EspecificacionLOM
from django.forms.extras.widgets import SelectDateWidget

class EspecificacionForm(ModelForm):
	class Meta:
		model=EspecificacionLOM
	fecha = forms.DateField(initial=datetime.date.today,widget=SelectDateWidget())
	derechos = forms.CharField()