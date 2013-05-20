#encoding:utf-8
from django.forms import ModelForm, Textarea, TextInput
from django import forms
import datetime
from django.contrib.admin.widgets import AdminFileWidget
#from django.forms.widgets import ClearableFileInput
from gestorObjetos.models import EspecificacionLOM, Objeto, Repositorio, PalabraClave
import siova.lib.Opciones as opc
"""
Formulario basado en el modelo EspecificacionLOM
"""
class EspecificacionForm(ModelForm):
	class Meta:
		model=EspecificacionLOM
		#modificación de cada uno de los campos que se muestran en la plantilla para que tengan un tamaño fijo
		widgets = {
			'lc1_titulo': TextInput(attrs={'size': 40}),
            'lc1_descripcion': Textarea(attrs={'cols': 40, 'rows': 5}),
            'lc1_cobertura': Textarea(attrs={'cols': 40, 'rows': 5}),
            'lc2_version': TextInput(attrs={'size': 40}),
            'lc3_requerimientos': Textarea(attrs={'cols': 40, 'rows': 5}),
            'lc3_instrucciones': Textarea(attrs={'cols': 40, 'rows': 5}),
            'lc4_poblacion': Textarea(attrs={'cols': 40, 'rows': 5}),
            'lc5_derechos': Textarea(attrs={'cols': 40, 'rows': 5}),
            'lc6_uso_educativo': Textarea(attrs={'cols': 40, 'rows': 5}),
        }
    # Reemplazo del campo de idioma para que tenga un comportamiento común
	lc1_idioma = forms.CharField(max_length=2,widget=forms.Select(choices=opc.get_idiomas()), label="Idioma", help_text='Lenguaje predominante en el objeto')
	# Reemplazo del campo de Fecha con elfin de colocar un valor inicial
	lc2_fecha = forms.DateField(initial=datetime.date.today, label="Fecha de Publicación", help_text='Fecha en que el objeto es publicado')

"""
Creación de un formulario para las consultas avanzadas de objetos.
"""
class cEspecificacionForm(forms.Form):
	c_titulo = forms.CharField(max_length=200)
	c_tipo_obj = forms.CharField(max_length=3,widget=forms.Select(choices=opc.get_tipo_obj()))
	c_idioma = forms.CharField(max_length=2,widget=forms.Select(choices=opc.get_idiomas()))
	c_nivel_agregacion = forms.CharField(max_length=2,widget=forms.Select(choices=opc.get_nivel_agregacion()))
	c_fecha = forms.DateField(initial=datetime.date.today)
	c_tipo_inter = forms.CharField(max_length=3,widget=forms.Select(choices=opc.get_tipo_interactividad()))
	c_tipo_rec = forms.CharField(max_length=50,widget=forms.Select(choices=opc.get_tipo_recurso()))
	c_nivel_inter = forms.CharField(max_length=3,widget=forms.Select(choices=opc.get_nivel_interactividad()))


"""
Formulario basado en el modelo Objeto
"""
class ObjetosForm(ModelForm):
	#función constructora que modifica el query para que en el campo de repositorio solo aparezcan/
	#los grupos del respectivo usuario docente.
	def __init__(self,gruposu,*args,**kwargs):
		super (ObjetosForm,self ).__init__(*args,**kwargs)
		self.fields['repositorio'].queryset = Repositorio.objects.filter(grupos=gruposu)
	class Meta:
		model=Objeto
		#Se excluye los campos con dependencias a los models EspecificacioLOM, Autores y Usuario Creador
		exclude = ('espec_lom','autores','creador')
	#Se modifica el comportamiento de estos campos
	palabras_claves = forms.CharField(max_length=500, required=False, label="Palabras", help_text='Palabras Asociadas al Objeto')
	archivo = forms.FileField(widget=AdminFileWidget, label="Archivo", help_text='Archivo del Objeto')

"""
Creación de formulario para incluir los campos en la consulta avanzada de objetos.
"""
class cObjetosForm(ModelForm):
	#Función construtura que modifica el query de repositorios dependiendo del usuario y coloca las palabra claves previas como dato inicial
	def __init__(self,usuario,objeto,*args,**kwargs):
		super (cObjetosForm,self ).__init__(*args,**kwargs)
		palabras=objeto.palabras_claves.all()
		self.fields['repositorio'].queryset = Repositorio.objects.filter(grupos=usuario.groups.all())
		self.fields['palabras_claves'].initial = ' '.join(str(n) for n in palabras)
	class Meta:
		model=Objeto
		# Se exluyen los siguientes campos que forman dependencias con sus respectivos modelos
		exclude =('espec_lom','autores','creador', 'palabras_claves')
	#Se crean los campos específicos para mostrar un comportamiento distinto al esperado.
	palabras_claves = forms.CharField(max_length=500, required=False, label="Palabras", help_text='Palabras Asociadas al Objeto')
	archivo= forms.FileField(widget=AdminFileWidget, label="Archivo", help_text='Archivo del Objeto')