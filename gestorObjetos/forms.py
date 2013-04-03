#encoding:utf-8
from django.forms import ModelForm
from django import forms
import datetime
from gestorObjetos.models import EspecificacionLOM, Objeto, Repositorio
from django.forms.extras.widgets import SelectDateWidget

class EspecificacionForm(ModelForm):
	class Meta:
		model=EspecificacionLOM
	fecha = forms.DateField(initial=datetime.date.today,widget=SelectDateWidget())
	derechos = forms.CharField()

class cEspecificacionForm(ModelForm):
	class Meta:
		model=EspecificacionLOM
	lc2_fecha = forms.DateField(initial=datetime.date.today)

class ObjetosForm(ModelForm):
	def __init__(self,gruposu,*args,**kwargs):
		super (ObjetosForm,self ).__init__(*args,**kwargs) # populates the post
		self.fields['repositorio'].queryset = Repositorio.objects.filter(grupos=gruposu)
	class Meta:
		model=Objeto
		exclude = ('espec_lom','autores',)
	palabras_claves = forms.CharField(max_length=500, required=False)