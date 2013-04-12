#encoding:utf-8
from django.forms import ModelForm, Textarea
from django import forms
import datetime
from gestorObjetos.models import EspecificacionLOM, Objeto, Repositorio, PalabraClave
import siova.lib.Opciones as opc

class EspecificacionForm(ModelForm):
	class Meta:
		model=EspecificacionLOM
		widgets = {
            'lc1_descripcion': Textarea(attrs={'cols': 35, 'rows': 5}),
            'lc1_cobertura': Textarea(attrs={'cols': 35, 'rows': 5}),
            'lc3_requerimientos': Textarea(attrs={'cols': 35, 'rows': 5}),
            'lc3_instrucciones': Textarea(attrs={'cols': 35, 'rows': 5}),
            'lc4_poblacion': Textarea(attrs={'cols': 35, 'rows': 5}),
            'lc5_derechos': Textarea(attrs={'cols': 35, 'rows': 5}),
            'lc6_uso_educativo': Textarea(attrs={'cols': 35, 'rows': 5}),
        }
	lc1_idioma = forms.CharField(max_length=2,widget=forms.Select(choices=opc.get_idiomas()))
	lc2_fecha = forms.DateField(initial=datetime.date.today)

class cEspecificacionForm(forms.Form):
	c_titulo = forms.CharField(max_length=200)
	c_tipo_obj = forms.CharField(max_length=3,widget=forms.Select(choices=opc.get_tipo_obj()))
	c_idioma = forms.CharField(max_length=2,widget=forms.Select(choices=opc.get_idiomas()))
	c_nivel_agregacion = forms.CharField(max_length=2,widget=forms.Select(choices=opc.get_nivel_agregacion()))
	c_fecha = forms.DateField(initial=datetime.date.today)
	c_tipo_inter = forms.CharField(max_length=3,widget=forms.Select(choices=opc.get_tipo_interactividad()))
	c_tipo_rec = forms.CharField(max_length=50,widget=forms.Select(choices=opc.get_tipo_recurso()))
	c_nivel_inter = forms.CharField(max_length=3,widget=forms.Select(choices=opc.get_nivel_interactividad()))

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