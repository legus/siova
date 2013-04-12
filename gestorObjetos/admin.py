from gestorObjetos.models import Objeto, EspecificacionLOM, Repositorio, PalabraClave, Autor, RutaCategoria, UserProfile
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
 
admin.site.unregister(User)
 
class UserProfileInline(admin.StackedInline):
	model = UserProfile
 
class UserProfileAdmin(UserAdmin):
	inlines = [UserProfileInline]
 
class ObjetoAdmin(admin.ModelAdmin):
    list_display = ('espec_lom', 'tipo_obj', 'publicado')
    search_fields = ('espec_lom__lc1_titulo', 'palabras_claves__palabra_clave', 'espec_lom__lc1_descripcion', 'autores__nombres', 'autores__apellidos', 'autores__rol')
    list_filter = ('repositorio','creador','espec_lom__lc1_idioma','espec_lom__lc4_contexto','espec_lom__lc4_tipo_rec','ruta_categoria')
    filter_horizontal = ('autores','palabras_claves')
    raw_id_fields = ('creador','ruta_categoria')

class AutorAdmin(admin.ModelAdmin):
	list_filter = ('rol',)

class RepositorioAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'publico')
	list_filter = ('grupos','publico')

class EspecificacionLOMAdmin(admin.ModelAdmin):
    list_display = ('lc1_titulo', 'lc2_version')
    search_fields = ('lc1_titulo', 'lc1_descripcion','lc1_cobertura','lc4_poblacion','lc5_derechos',' lc6_uso_educativo')
    list_filter = ('lc1_idioma','lc4_contexto','lc4_tipo_rec','lc1_nivel_agregacion','lc4_nivel_inter')
    date_hierarchy = 'lc2_fecha'
 
admin.site.register(User, UserProfileAdmin)

admin.site.register(Objeto, ObjetoAdmin)
admin.site.register(EspecificacionLOM, EspecificacionLOMAdmin)
admin.site.register(Repositorio, RepositorioAdmin)
admin.site.register(PalabraClave)
admin.site.register(Autor, AutorAdmin)
admin.site.register(RutaCategoria)