#encoding:utf-8
from django.forms import ModelForm
from django import forms
import datetime
from gestorObjetos.models import EspecificacionLOM, Objeto, Repositorio, PalabraClave
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
		super (ObjetosForm,self ).__init__(*args,**kwargs)
		self.fields['repositorio'].queryset = Repositorio.objects.filter(grupos=gruposu)
	class Meta:
		model=Objeto
		exclude = ('espec_lom','autores',)
	palabras_claves = forms.CharField(max_length=500, required=False)

class cObjetosForm(ModelForm):
	def __init__(self,usuario,objeto,*args,**kwargs):
		super (cObjetosForm,self ).__init__(*args,**kwargs)
		palabras=objeto.palabras_claves.all()
		self.fields['repositorio'].queryset = Repositorio.objects.filter(grupos=usuario.groups.all())
		self.fields['palabras_claves'].initial = ' '.join(str(n) for n in palabras)
	class Meta:
		model=Objeto
		exclude =('espec_lom','autores','palabras_claves','creador')
	palabras_claves = forms.CharField(max_length=500, required=False)