#encoding:utf-8
from gestorProyectos.models import Proyecto, Facultad, Programa, Grado, Factor_competencias, Enunciado, Indicador, Parametro, Validacion, OperacionMental
from django.contrib import admin

"""
Clase que permite sobre-escribir la clase Programa en la interfaz de administración de django.
Esto con el fin de modificar las columnas de visualización y los filtros
"""
class ProgramaAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'sede')	
	search_fields = ('nombre', 'sede', 'modalidad')
	list_filter = ('modalidad', 'sede','facultad')

"""
Clase que permite sobre-escribir la clase Proyecto en la interfaz de administración de django.
Esto con el fin de modificar las columnas de visualización y los filtros
"""
class ProyectoAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'fase', 'calificacion', 'nota')
	search_fields = ('titulo', 'programa__nombre')
	list_filter = ('programa__nombre', 'fase', 'calificacion')
	filter_horizontal =('indicadores','operaciones')
	date_hierarchy = 'fecha'

"""
Clase que permite sobre-escribir la clase Validación en la interfaz de administración de django.
Esto con el fin de modificar las columnas de visualización y los filtros
"""
class ValidacionAdmin(admin.ModelAdmin):
	list_display = ('parametro', 'valoracion')
	list_filter = ('proyecto__titulo', 'parametro__tipo', 'parametro__nombre')
	date_hierarchy = 'fecha'

"""
Clase que permite sobre-escribir la clase Factor_competencias en la interfaz de administración de django.
Esto con el fin de modificar las columnas de visualización y los filtros
"""
class Factor_competenciasAdmin(admin.ModelAdmin):
	search_fields = ('factor',)
	list_filter = ('ruta_categoria__nombre_ruta',)

"""
Clase que permite sobre-escribir la clase Enunciado en la interfaz de administración de django.
Esto con el fin de modificar las columnas de visualización y los filtros
"""
class EnunciadoAdmin(admin.ModelAdmin):
	search_fields = ('enunciado', 'factor__factor')
	list_filter = ('factor__factor',)

"""
Clase que permite sobre-escribir la clase Indicadores en la interfaz de administración de django.
Esto con el fin de modificar las columnas de visualización y los filtros
"""
class IndicadorAdmin(admin.ModelAdmin):
	search_fields = ('indicador', 'factor__factor','enunciado__enunciado')
	list_filter = ('grados__nominacion', 'factor__factor', 'enunciado__enunciado')

"""
Clase que permite sobre-escribir la clase Parametro en la interfaz de administración de django.
Esto con el fin de modificar las columnas de visualización y los filtros
"""
class ParametroAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'ponderacion')
	list_filter = ('tipo',)


admin.site.register(Proyecto, ProyectoAdmin),
admin.site.register(Facultad),
admin.site.register(Programa, ProgramaAdmin),
admin.site.register(Grado),
admin.site.register(Factor_competencias, Factor_competenciasAdmin),
admin.site.register(Enunciado, EnunciadoAdmin),
admin.site.register(Indicador, IndicadorAdmin),
admin.site.register(Parametro, ParametroAdmin),
admin.site.register(Validacion, ValidacionAdmin)
admin.site.register(OperacionMental)